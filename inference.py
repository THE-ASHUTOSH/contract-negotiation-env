import os
import json
import httpx
from openai import OpenAI

API_BASE_URL = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct")
HF_TOKEN = os.environ.get("HF_TOKEN", "not-needed")
BASE_URL = os.environ.get("SPACE_URL", "http://localhost:8000")

llm = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

SYSTEM_PROMPT = """You are an autonomous contract negotiation agent. You will be given two versions of a contract.
Your job is to negotiate them step by step.

Available actions:
1. identify_conflicts — list all clause IDs that conflict between the two versions
2. propose_compromise — propose new compromise text for a specific conflicting clause
3. accept_clause — accept the vendor or client version of a non-conflicting clause
4. flag_non_negotiable — flag a clause you believe is non-negotiable
5. finalize_contract — submit the complete merged final contract text

ALWAYS respond with a single valid JSON object. No text outside the JSON.

Format:
{
  "action_type": "<one of the 5 types above>",
  "episode_id": "<episode_id from observation>",
  "clause_ids": ["clause_1", "clause_2"],
  "clause_id": "clause_1",
  "proposed_text": "...",
  "accept_from": "vendor",
  "final_contract": "..."
}

Only include the fields relevant to the chosen action_type. Do not include null or unused fields."""


TASKS = ["task_easy", "task_medium", "task_hard"]


def build_initial_prompt(obs: dict) -> str:
    """Format the initial observation into a readable prompt for the LLM."""
    observation = obs.get("observation", obs)
    vendor = observation.get("vendor_contract", "")
    client = observation.get("client_contract", "")
    task_id = observation.get("task_id", "")
    max_steps = observation.get("max_steps", 12)

    return f"""Task: {task_id}
Max Steps: {max_steps}

=== VENDOR CONTRACT ===
{vendor}

=== CLIENT CONTRACT ===
{client}

Review both contracts carefully. Start by identifying all conflicting clauses using the identify_conflicts action. List every clause_id where the vendor and client versions differ."""


def parse_action(text: str) -> dict:
    """Extract JSON action from LLM response text."""
    text = text.strip()

    # Remove markdown code fences if present
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{"):
                text = part
                break

    # Try to find JSON object in the text
    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        text = text[start:end]

    return json.loads(text)


def format_feedback(result: dict) -> str:
    """Format step result as feedback for the LLM."""
    observation = result.get("observation", result)
    reward = result.get("reward", observation.get("reward", 0.0))
    done = result.get("done", observation.get("done", False))
    message = observation.get("message", "")

    parts = [f"Result: {message}", f"Reward: {reward:.2f}", f"Done: {done}"]

    if observation.get("identified_conflicts"):
        parts.append(f"Identified conflicts: {json.dumps(observation['identified_conflicts'])}")

    if observation.get("grader_feedback"):
        parts.append(f"Grader feedback: {json.dumps(observation['grader_feedback'])}")

    if observation.get("error_message"):
        parts.append(f"Error: {observation['error_message']}")

    if not done:
        step = observation.get("current_step", 0)
        max_steps = observation.get("max_steps", 12)
        remaining = max_steps - step
        parts.append(f"Steps remaining: {remaining}")
        if remaining <= 2:
            parts.append("WARNING: Running low on steps. Consider finalizing the contract soon with finalize_contract action.")
        elif remaining <= 1:
            parts.append("CRITICAL: This is your last step. You MUST submit finalize_contract now.")

    return "\n".join(parts)


def run_task(task_id: str):
    """Run a single task through the negotiation loop."""
    print(f"[START] task={task_id} env=contract-negotiation-env model={MODEL_NAME}")

    try:
        reset_response = httpx.post(
            f"{BASE_URL}/reset",
            json={"task_id": task_id},
            timeout=30.0,
        )
        reset_response.raise_for_status()
        obs = reset_response.json()
    except Exception as e:
        err_msg = str(e).replace("\n", " ")[:200]
        print(f'[STEP] step=1 action={json.dumps({})} reward=0.00 done=true error={err_msg}')
        print(f"[END] success=false steps=0 score=0.000 rewards=")
        return

    # Get episode_id from state endpoint since reset response doesn't include it
    try:
        state_response = httpx.get(f"{BASE_URL}/state", timeout=10.0)
        state_data = state_response.json()
        episode_id = state_data.get("episode_id", "")
    except Exception:
        episode_id = ""
    max_steps = obs.get("observation", obs).get("max_steps", 12)

    conversation = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_initial_prompt(obs)},
    ]

    step = 0
    all_rewards = []
    done = False
    success = False

    while not done and step < max_steps:
        step += 1
        error = "null"
        action_dict = {}
        reward = 0.0

        try:
            # Call LLM with retries for JSON parse failures
            llm_text = None
            for attempt in range(3):
                try:
                    response = llm.chat.completions.create(
                        model=MODEL_NAME,
                        messages=conversation,
                        max_tokens=1500,
                        temperature=0.1,
                    )
                    llm_text = response.choices[0].message.content.strip()
                    action_dict = parse_action(llm_text)
                    break
                except json.JSONDecodeError:
                    if attempt < 2:
                        # Ask LLM to fix its JSON
                        conversation.append({"role": "assistant", "content": llm_text or ""})
                        conversation.append({"role": "user", "content": "Your response was not valid JSON. Please respond with ONLY a valid JSON object, no other text."})
                    else:
                        raise

            conversation.append({"role": "assistant", "content": llm_text})

            # Ensure episode_id is set
            action_dict["episode_id"] = episode_id

            # Step environment
            step_response = httpx.post(
                f"{BASE_URL}/step",
                json={"action": action_dict},
                timeout=60.0,
            )
            step_response.raise_for_status()
            result = step_response.json()

            observation = result.get("observation", result)
            reward = result.get("reward", observation.get("reward", 0.0))
            if reward is None:
                reward = 0.0
            reward = max(0.0, min(1.0, float(reward)))
            done = result.get("done", observation.get("done", False))
            all_rewards.append(reward)

            # Feed observation back to LLM
            conversation.append({"role": "user", "content": format_feedback(result)})

            if done and reward > 0.3:
                success = True

        except Exception as e:
            error = str(e).replace("\n", " ")[:200]
            all_rewards.append(0.0)
            reward = 0.0

        print(f"[STEP] step={step} action={json.dumps(action_dict)} reward={reward:.2f} done={str(done).lower()} error={error}")

    final_score = sum(all_rewards) / len(all_rewards) if all_rewards else 0.0
    print(f"[END] success={str(success).lower()} steps={step} score={final_score:.3f} rewards={','.join(f'{r:.2f}' for r in all_rewards)}")


def main():
    for task_id in TASKS:
        run_task(task_id)


if __name__ == "__main__":
    main()
