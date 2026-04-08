import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from server.graders import grade_conflict_identification, grade_final_contract


def test_f1_perfect():
    predicted = ["clause_2", "clause_4", "clause_5"]
    truth = ["clause_2", "clause_4", "clause_5"]
    assert 0.9 < grade_conflict_identification(predicted, truth) < 1.0


def test_f1_zero():
    predicted = ["clause_1", "clause_3"]
    truth = ["clause_2", "clause_4", "clause_5"]
    assert 0.0 < grade_conflict_identification(predicted, truth) < 0.1


def test_f1_half_recall():
    predicted = ["clause_2"]
    truth = ["clause_2", "clause_4"]
    score = grade_conflict_identification(predicted, truth)
    # precision = 1.0, recall = 0.5, f1 = 2/3
    assert 0.0 < score < 1.0
    assert abs(score - 2 / 3) < 0.01


def test_f1_empty_predicted():
    predicted = []
    truth = ["clause_2", "clause_4", "clause_5"]
    assert 0.0 < grade_conflict_identification(predicted, truth) < 0.1


def test_final_contract_score_range():
    """Test that grade_final_contract returns a float in [0.0, 1.0].
    Uses a mock LLM client to avoid network calls."""

    class MockChoice:
        def __init__(self):
            self.message = type("obj", (object,), {"content": '{"score": 0.7, "resolved": true}'})()

    class MockResponse:
        def __init__(self):
            self.choices = [MockChoice()]

    class MockCompletions:
        def create(self, **kwargs):
            return MockResponse()

    class MockChat:
        def __init__(self):
            self.completions = MockCompletions()

    class MockLLM:
        def __init__(self):
            self.chat = MockChat()

    from server.contract_fixtures import TASK_FIXTURES

    fixture = TASK_FIXTURES["task_easy"]
    mock_llm = MockLLM()
    score = grade_final_contract(
        "Payment Terms: Net-45. Liability Cap: $30,000. Termination: 60 days.",
        fixture,
        mock_llm,
        "test-model",
    )
    assert isinstance(score, float)
    assert 0.0 < score < 1.0
