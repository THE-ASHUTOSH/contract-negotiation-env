---
title: Contract Negotiation Env
emoji: 📝
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 8000
pinned: false
---

# Autonomous Contract Negotiation Agent

## Project Overview

An OpenEnv RL environment where an LLM agent autonomously negotiates contracts end-to-end. The agent reads conflicting vendor and client contracts, identifies all conflicting clauses, proposes legally consistent compromise language, flags non-negotiable terms, and produces a merged final contract — with zero human intervention.

## Real-World Use Case

Contract negotiation is one of the most time-consuming tasks in business operations. Legal teams spend hundreds of hours redlining contracts, comparing clause language, and negotiating terms. An autonomous agent that can identify conflicts, propose fair compromises, and produce a merged agreement could dramatically reduce negotiation cycles from weeks to minutes, while ensuring consistency and reducing human error.

## Environment Architecture

The environment follows a client-server architecture:

- **Server** (`server/app.py`): FastAPI-based HTTP server that manages the negotiation environment state. Exposes `/health`, `/reset`, `/step`, and `/state` endpoints.
- **Client** (`client.py`): WebSocket-based client that wraps the OpenEnv `EnvClient` for programmatic access.
- **Inference** (`inference.py`): Standalone agent loop that communicates with the server via HTTP, calling an LLM to decide actions at each step.

## Action Space

| Action Type | Fields | Description |
|---|---|---|
| `identify_conflicts` | `clause_ids: List[str]` | Identify all clause IDs that conflict between vendor and client |
| `propose_compromise` | `clause_id: str`, `proposed_text: str` | Propose new compromise text for a conflicting clause |
| `accept_clause` | `clause_id: str`, `accept_from: str` | Accept the vendor or client version of a clause |
| `flag_non_negotiable` | `clause_id: str` | Flag a clause as non-negotiable |
| `finalize_contract` | `final_contract: str` | Submit the complete merged final contract text |

## Observation Space

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | Whether the action succeeded |
| `message` | `str` | Human-readable status message |
| `reward` | `float` | Reward for the current step (0.0-1.0) |
| `done` | `bool` | Whether the episode has ended |
| `task_id` | `str` | Current task identifier |
| `current_step` | `int` | Current step number |
| `max_steps` | `int` | Maximum allowed steps |
| `vendor_contract` | `str` | Full vendor contract text (on reset) |
| `client_contract` | `str` | Full client contract text (on reset) |
| `identified_conflicts` | `List[Dict]` | Results of conflict identification |
| `proposed_compromises` | `List[Dict]` | Proposed compromise details |
| `merged_contract` | `str` | Final merged contract (on finalize) |
| `grader_feedback` | `Dict` | Scoring feedback from grader |
| `error_message` | `str` | Error details if action failed |

## State Space

| Field | Type | Description |
|---|---|---|
| `episode_id` | `str` | Unique episode identifier |
| `task_id` | `str` | Current task |
| `step_count` | `int` | Steps taken so far |
| `max_steps` | `int` | Maximum steps allowed |
| `done` | `bool` | Episode completion flag |
| `total_reward` | `float` | Cumulative reward |
| `rewards_per_step` | `List[float]` | Reward history |
| `conflicts_identified` | `List[Dict]` | Identified conflicts |
| `compromises_proposed` | `List[Dict]` | Proposed compromises |
| `accepted_clauses` | `List[Dict]` | Accepted clauses |
| `non_negotiable_flags` | `List[str]` | Flagged non-negotiable clauses |
| `final_contract_submitted` | `bool` | Whether final contract was submitted |
| `final_contract_text` | `str` | The submitted final contract |

## Tasks

- **task_easy** — *Clause Conflict Identification*: Simple 6-clause Software Service Agreement with 3 conflicts (payment terms, liability cap, termination notice). No non-negotiables. Max 5 steps.
- **task_medium** — *Compromise Language Proposal*: 8-clause GDPR-style Data Processing Agreement with 4 conflicts (data retention, sub-processor approval, breach notification, audit rights). Data retention clause is non-negotiable. Max 8 steps.
- **task_hard** — *Full Autonomous Contract Merger*: 12-clause Enterprise Technology Partnership Agreement with 6 conflicts (IP ownership, revenue share, exclusivity, governing law, SLA penalties, force majeure). IP ownership and governing law are non-negotiable. Max 12 steps.

## Reward Function

| Action | Scoring Method |
|---|---|
| `identify_conflicts` | F1 score (precision × recall) against ground truth conflict list |
| `propose_compromise` | LLM-as-judge: interests addressed (0.4), legal clarity (0.3), genuine compromise (0.3) |
| `accept_clause` | 1.0 for non-negotiable, 0.8 for non-conflicting, 0.3 for conflicting (penalizes lazy acceptance) |
| `flag_non_negotiable` | 1.0 if clause is truly non-negotiable, 0.0 otherwise |
| `finalize_contract` | Composite: completeness (0.30) + conflict resolution (0.30) + non-negotiable respect (0.20) + coherence (0.20) |

## Quick Start (Local)

```bash
pip install -e .
uvicorn server.app:app --port 8000
python inference.py
```

## Docker Run

```bash
docker build -t contract-negotiation-env .
docker run -p 8000:8000 \
  -e HF_TOKEN=your_token \
  -e MODEL_NAME=meta-llama/Llama-3.3-70B-Instruct \
  contract-negotiation-env
```

## HF Spaces Deployment

1. Create a new Hugging Face Space (Docker SDK)
2. Upload all project files
3. Set environment variables: `HF_TOKEN`, `MODEL_NAME`, `API_BASE_URL`
4. The Space will build the Docker image and start the server on port 8000
5. Use the Space URL as `SPACE_URL` when running `inference.py`

## Sample Episode Output

```
[START] task=task_easy env=contract-negotiation-env model=meta-llama/Llama-3.3-70B-Instruct
[STEP] step=1 action={"action_type": "identify_conflicts", "clause_ids": ["clause_2", "clause_4", "clause_5"]} reward=1.00 done=false error=null
[STEP] step=2 action={"action_type": "propose_compromise", "clause_id": "clause_2", "proposed_text": "..."} reward=0.75 done=false error=null
[STEP] step=3 action={"action_type": "finalize_contract", "final_contract": "..."} reward=0.80 done=true error=null
[END] success=true steps=3 score=0.850 rewards=1.00,0.75,0.80
```
