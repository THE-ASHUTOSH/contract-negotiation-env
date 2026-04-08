from typing import Dict, Any

from openenv.core.env_client import EnvClient, StepResult
from models import ContractAction, ContractObservation, ContractState


class ContractNegotiationEnv(EnvClient[ContractAction, ContractObservation, ContractState]):

    def _step_payload(self, action: ContractAction) -> Dict[str, Any]:
        data = action.model_dump()
        return {k: v for k, v in data.items() if v is not None}

    def _parse_result(self, payload: Dict[str, Any]) -> StepResult[ContractObservation]:
        obs_data = payload.get("observation", payload)
        observation = ContractObservation(**obs_data)
        return StepResult(
            observation=observation,
            reward=payload.get("reward", observation.reward),
            done=payload.get("done", observation.done),
        )

    def _parse_state(self, payload: Dict[str, Any]) -> ContractState:
        return ContractState(**payload)
