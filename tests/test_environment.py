import os
import sys
import pytest

# Ensure project root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from server.environment import ContractNegotiationEnvironment
from models import ContractAction


@pytest.fixture
def env():
    return ContractNegotiationEnvironment()


def test_reset_easy_returns_contracts(env):
    obs = env.reset(task_id="task_easy")
    assert obs.vendor_contract is not None and len(obs.vendor_contract) > 0
    assert obs.client_contract is not None and len(obs.client_contract) > 0
    assert obs.done is False
    assert obs.task_id == "task_easy"


def test_reset_hard_returns_contracts(env):
    obs = env.reset(task_id="task_hard")
    assert obs.vendor_contract is not None and len(obs.vendor_contract) > 0
    assert obs.client_contract is not None and len(obs.client_contract) > 0
    assert obs.done is False
    assert obs.task_id == "task_hard"


def test_step_identify_conflicts_perfect(env):
    env.reset(task_id="task_easy")
    action = ContractAction(
        action_type="identify_conflicts",
        episode_id=env.state.episode_id,
        clause_ids=["clause_2", "clause_4", "clause_5"],
    )
    obs = env.step(action)
    assert 0.9 < obs.reward < 1.0
    assert obs.success is True


def test_step_identify_conflicts_empty(env):
    env.reset(task_id="task_easy")
    action = ContractAction(
        action_type="identify_conflicts",
        episode_id=env.state.episode_id,
        clause_ids=[],
    )
    obs = env.step(action)
    assert 0.0 < obs.reward < 0.1


def test_step_finalize_produces_valid_score(env):
    env.reset(task_id="task_easy")
    # First identify conflicts (burns a step)
    action = ContractAction(
        action_type="identify_conflicts",
        episode_id=env.state.episode_id,
        clause_ids=["clause_2", "clause_4", "clause_5"],
    )
    env.step(action)
    # Then finalize with some contract text
    action = ContractAction(
        action_type="finalize_contract",
        episode_id=env.state.episode_id,
        final_contract="MERGED CONTRACT\n\nClause 1 - Scope of Services: unchanged.\n\nClause 2 - Payment Terms: Net-45 compromise.\n\nClause 3 - Term: unchanged.\n\nClause 4 - Liability Cap: $30,000 compromise.\n\nClause 5 - Termination: 60 days notice compromise.\n\nClause 6 - Confidentiality: unchanged.",
    )
    obs = env.step(action)
    assert 0.0 <= obs.reward <= 1.0
    assert obs.done is True


def test_max_steps_terminates(env):
    env.reset(task_id="task_easy")
    # task_easy has max_steps=5
    for i in range(6):
        action = ContractAction(
            action_type="identify_conflicts",
            episode_id=env.state.episode_id,
            clause_ids=["clause_2"],
        )
        obs = env.step(action)
    assert obs.done is True


def test_invalid_action_returns_error(env):
    env.reset(task_id="task_easy")
    action = ContractAction(
        action_type="invalid",
        episode_id=env.state.episode_id,
    )
    obs = env.step(action)
    assert obs.error_message is not None


def test_done_episode_rejects_steps(env):
    env.reset(task_id="task_easy")
    # Finalize to end the episode
    action = ContractAction(
        action_type="finalize_contract",
        episode_id=env.state.episode_id,
        final_contract="Final merged contract text.",
    )
    obs = env.step(action)
    assert obs.done is True

    # Try stepping again
    action = ContractAction(
        action_type="identify_conflicts",
        episode_id=env.state.episode_id,
        clause_ids=["clause_2"],
    )
    obs = env.step(action)
    assert obs.done is True
    assert obs.error_message is not None
