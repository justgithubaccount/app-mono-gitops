import pytest
from app.behavior import BehaviorDefinition


def test_valid_behavior():
    data = {
        "agents": [
            {
                "role": "researcher",
                "goal": "find info",
            }
        ],
        "tasks": [
            {
                "description": "collect",
                "expected_output": "summary"
            }
        ],
        "process": "sequential"
    }

    model = BehaviorDefinition.model_validate(data)
    assert model.agents[0].role == "researcher"
    assert model.tasks[0].description == "collect"


def test_invalid_behavior():
    data = {"agents": [{"goal": "missing role"}]}
    with pytest.raises(Exception):
        BehaviorDefinition.model_validate(data)
