import uvicorn
from openenv.core.env_server import create_app
from server.environment import ContractNegotiationEnvironment
from models import ContractAction, ContractObservation

_singleton_env = ContractNegotiationEnvironment()


def _env_factory():
    return _singleton_env


app = create_app(
    env=_env_factory,
    action_cls=ContractAction,
    observation_cls=ContractObservation,
    env_name="contract-negotiation-env",
)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
