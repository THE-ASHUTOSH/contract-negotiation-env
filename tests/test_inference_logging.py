import re
import pytest


def test_start_format():
    line = "[START] task=task_easy env=contract-negotiation-env model=meta-llama/Llama-3.3-70B-Instruct"
    assert re.match(r"\[START\] task=\S+ env=contract-negotiation-env model=\S+", line)


def test_step_format():
    line = '[STEP] step=1 action={"action_type": "identify_conflicts"} reward=0.85 done=false error=null'
    assert re.match(r"\[STEP\] step=\d+ action=.+ reward=[\d.]+ done=(true|false) error=.+", line)


def test_end_format():
    line = "[END] success=true steps=3 score=0.750 rewards=0.85,0.70,0.65"
    assert re.match(r"\[END\] success=(true|false) steps=\d+ score=[\d.]+ rewards=[\d.,]+", line)
