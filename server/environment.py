import os
import uuid
from typing import Optional, Any

from openai import OpenAI
from openenv.core.env_server import Environment

from models import ContractAction, ContractObservation, ContractState
from server.contract_fixtures import TASK_FIXTURES
from server.graders import grade_conflict_identification, grade_compromise, grade_final_contract


def _strict_clamp(reward: float) -> float:
    """Clamp reward to strictly (0, 1) — never exactly 0.0 or 1.0."""
    return max(0.01, min(0.99, float(reward)))


class ContractNegotiationEnvironment(Environment[ContractAction, ContractObservation, ContractState]):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._state = ContractState()
        self._fixture = None
        self._llm = OpenAI(
            base_url=os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1"),
            api_key=os.environ.get("HF_TOKEN", "not-needed"),
        )
        self._model = os.environ.get("MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct")

    def reset(
        self,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
        task_id: str = "task_easy",
        **kwargs: Any,
    ) -> ContractObservation:
        ep_id = episode_id or str(uuid.uuid4())
        self._fixture = TASK_FIXTURES[task_id]

        self._state = ContractState(
            episode_id=ep_id,
            task_id=task_id,
            step_count=0,
            max_steps=self._fixture["max_steps"],
            done=False,
            total_reward=0.0,
            rewards_per_step=[],
            conflicts_identified=[],
            compromises_proposed=[],
            accepted_clauses=[],
            non_negotiable_flags=[],
            final_contract_submitted=False,
            final_contract_text=None,
        )

        return ContractObservation(
            success=True,
            message=f"Environment reset for {task_id}. Review the vendor and client contracts and begin negotiation.",
            reward=0.0,
            done=False,
            task_id=task_id,
            current_step=0,
            max_steps=self._fixture["max_steps"],
            vendor_contract=self._fixture["vendor_contract"],
            client_contract=self._fixture["client_contract"],
        )

    def step(
        self,
        action: ContractAction,
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> ContractObservation:
        # Guard: already done
        if self._state.done:
            return ContractObservation(
                success=False,
                message="Episode is already complete.",
                reward=0.0,
                done=True,
                task_id=self._state.task_id,
                current_step=self._state.step_count,
                max_steps=self._state.max_steps,
                error_message="Episode is already done. Call reset() to start a new episode.",
            )

        # Guard: max steps
        if self._state.step_count >= self._state.max_steps:
            self._state.done = True
            return ContractObservation(
                success=False,
                message="Max steps reached. Episode terminated.",
                reward=0.0,
                done=True,
                task_id=self._state.task_id,
                current_step=self._state.step_count,
                max_steps=self._state.max_steps,
                error_message="Max steps reached",
            )

        self._state.step_count += 1
        action_type = action.action_type

        try:
            if action_type == "identify_conflicts":
                return self._handle_identify_conflicts(action)
            elif action_type == "propose_compromise":
                return self._handle_propose_compromise(action)
            elif action_type == "accept_clause":
                return self._handle_accept_clause(action)
            elif action_type == "flag_non_negotiable":
                return self._handle_flag_non_negotiable(action)
            elif action_type == "finalize_contract":
                return self._handle_finalize_contract(action)
            else:
                return ContractObservation(
                    success=False,
                    message=f"Unknown action type: {action_type}",
                    reward=0.0,
                    done=False,
                    task_id=self._state.task_id,
                    current_step=self._state.step_count,
                    max_steps=self._state.max_steps,
                    error_message=f"Invalid action_type: {action_type}. Must be one of: identify_conflicts, propose_compromise, accept_clause, flag_non_negotiable, finalize_contract",
                )
        except Exception as e:
            self._state.rewards_per_step.append(0.01)
            return ContractObservation(
                success=False,
                message=f"Error processing action: {str(e)}",
                reward=0.01,
                done=False,
                task_id=self._state.task_id,
                current_step=self._state.step_count,
                max_steps=self._state.max_steps,
                error_message=str(e),
            )

    def _handle_identify_conflicts(self, action: ContractAction) -> ContractObservation:
        predicted = action.clause_ids or []
        ground_truth_ids = [c["clause_id"] for c in self._fixture["ground_truth_conflicts"]]

        reward = grade_conflict_identification(predicted, ground_truth_ids)
        reward = _strict_clamp(reward)

        identified = [{"clause_id": cid, "found": cid in ground_truth_ids} for cid in predicted]
        self._state.conflicts_identified = identified
        self._state.rewards_per_step.append(reward)
        self._state.total_reward += reward

        return ContractObservation(
            success=True,
            message=f"Identified {len(predicted)} conflicts. Score: {reward:.2f}",
            reward=reward,
            done=False,
            task_id=self._state.task_id,
            current_step=self._state.step_count,
            max_steps=self._state.max_steps,
            identified_conflicts=identified,
        )

    def _handle_propose_compromise(self, action: ContractAction) -> ContractObservation:
        clause_id = action.clause_id
        proposed_text = action.proposed_text or ""

        # Find the conflict
        conflict = None
        for c in self._fixture["ground_truth_conflicts"]:
            if c["clause_id"] == clause_id:
                conflict = c
                break

        if conflict is None:
            self._state.rewards_per_step.append(0.01)
            return ContractObservation(
                success=False,
                message=f"Clause {clause_id} not found in ground truth conflicts.",
                reward=0.01,
                done=False,
                task_id=self._state.task_id,
                current_step=self._state.step_count,
                max_steps=self._state.max_steps,
                error_message=f"Clause {clause_id} is not a recognized conflicting clause.",
            )

        reward = grade_compromise(
            clause_id, proposed_text,
            conflict["vendor_text"], conflict["client_text"],
            self._llm, self._model,
        )
        reward = _strict_clamp(reward)

        compromise_record = {
            "clause_id": clause_id,
            "proposed_text": proposed_text,
            "score": reward,
        }
        self._state.compromises_proposed.append(compromise_record)
        self._state.rewards_per_step.append(reward)
        self._state.total_reward += reward

        return ContractObservation(
            success=True,
            message=f"Compromise proposed for {clause_id}. Score: {reward:.2f}",
            reward=reward,
            done=False,
            task_id=self._state.task_id,
            current_step=self._state.step_count,
            max_steps=self._state.max_steps,
            grader_feedback={"clause_id": clause_id, "score": reward},
        )

    def _handle_accept_clause(self, action: ContractAction) -> ContractObservation:
        clause_id = action.clause_id or ""
        accept_from = action.accept_from or ""

        non_negotiable_list = self._fixture.get("non_negotiable_clauses", [])
        conflict_ids = [c["clause_id"] for c in self._fixture["ground_truth_conflicts"]]

        if clause_id in non_negotiable_list:
            # Accepting a non-negotiable clause from the original source is correct
            reward = 0.95
        elif clause_id in conflict_ids:
            # Accepting a conflicting clause without compromise is penalized
            reward = 0.30
        else:
            # Non-conflicting clause acceptance
            reward = 0.80

        reward = _strict_clamp(reward)

        self._state.accepted_clauses.append({
            "clause_id": clause_id,
            "accept_from": accept_from,
            "reward": reward,
        })
        self._state.rewards_per_step.append(reward)
        self._state.total_reward += reward

        return ContractObservation(
            success=True,
            message=f"Accepted {clause_id} from {accept_from}. Reward: {reward:.2f}",
            reward=reward,
            done=False,
            task_id=self._state.task_id,
            current_step=self._state.step_count,
            max_steps=self._state.max_steps,
        )

    def _handle_flag_non_negotiable(self, action: ContractAction) -> ContractObservation:
        clause_id = action.clause_id or ""
        non_negotiable_list = self._fixture.get("non_negotiable_clauses", [])

        reward = 0.95 if clause_id in non_negotiable_list else 0.05
        reward = _strict_clamp(reward)

        self._state.non_negotiable_flags.append(clause_id)
        self._state.rewards_per_step.append(reward)
        self._state.total_reward += reward

        return ContractObservation(
            success=True,
            message=f"Flagged {clause_id} as non-negotiable. Reward: {reward:.2f}",
            reward=reward,
            done=False,
            task_id=self._state.task_id,
            current_step=self._state.step_count,
            max_steps=self._state.max_steps,
        )

    def _handle_finalize_contract(self, action: ContractAction) -> ContractObservation:
        final_text = action.final_contract or ""

        reward = grade_final_contract(final_text, self._fixture, self._llm, self._model)
        reward = _strict_clamp(reward)

        self._state.done = True
        self._state.final_contract_submitted = True
        self._state.final_contract_text = final_text
        self._state.rewards_per_step.append(reward)
        self._state.total_reward += reward

        return ContractObservation(
            success=True,
            message=f"Contract finalized. Final score: {reward:.2f}",
            reward=reward,
            done=True,
            task_id=self._state.task_id,
            current_step=self._state.step_count,
            max_steps=self._state.max_steps,
            merged_contract=final_text,
        )

    @property
    def state(self) -> ContractState:
        return self._state
