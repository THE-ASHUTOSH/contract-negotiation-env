"""Task definitions for the contract negotiation environment."""

TASKS = {
    "task_easy": {
        "id": "task_easy",
        "name": "Clause Conflict Identification",
        "difficulty": "easy",
        "max_steps": 5,
        "reward_range": [0.0, 1.0],
        "description": "Identify conflicting clauses in a simple 6-clause Software Service Agreement.",
    },
    "task_medium": {
        "id": "task_medium",
        "name": "Compromise Language Proposal",
        "difficulty": "medium",
        "max_steps": 8,
        "reward_range": [0.0, 1.0],
        "description": "Negotiate a GDPR-style Data Processing Agreement with 4 conflicting clauses and non-negotiables.",
    },
    "task_hard": {
        "id": "task_hard",
        "name": "Full Autonomous Contract Merger",
        "difficulty": "hard",
        "max_steps": 12,
        "reward_range": [0.0, 1.0],
        "description": "Full negotiation and merger of a 12-clause Enterprise Technology Partnership Agreement.",
    },
}
