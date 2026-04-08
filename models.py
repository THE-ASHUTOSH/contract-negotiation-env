from typing import Optional, List, Dict
from openenv.core.env_server import Action, Observation, State
from pydantic import Field


class ContractAction(Action):
    action_type: str  # "identify_conflicts" | "propose_compromise" | "accept_clause" | "flag_non_negotiable" | "finalize_contract"
    episode_id: str = ""
    clause_ids: Optional[List[str]] = None
    clause_id: Optional[str] = None
    proposed_text: Optional[str] = None
    accept_from: Optional[str] = None  # "vendor" or "client"
    final_contract: Optional[str] = None


class ContractObservation(Observation):
    success: bool = True
    message: str = ""
    task_id: str = ""
    current_step: int = 0
    max_steps: int = 12
    vendor_contract: Optional[str] = None
    client_contract: Optional[str] = None
    identified_conflicts: Optional[List[Dict]] = None
    proposed_compromises: Optional[List[Dict]] = None
    merged_contract: Optional[str] = None
    grader_feedback: Optional[Dict] = None
    error_message: Optional[str] = None


class ContractState(State):
    task_id: str = ""
    max_steps: int = 12
    done: bool = False
    total_reward: float = 0.0
    rewards_per_step: List[float] = Field(default_factory=list)
    conflicts_identified: List[Dict] = Field(default_factory=list)
    compromises_proposed: List[Dict] = Field(default_factory=list)
    accepted_clauses: List[Dict] = Field(default_factory=list)
    non_negotiable_flags: List[str] = Field(default_factory=list)
    final_contract_submitted: bool = False
    final_contract_text: Optional[str] = None
