# tests/test_engineer_with_experience.py
import pytest
from unittest.mock import MagicMock, patch
from core.message import Message
from core.task import Task, TaskStatus
from core.experience import Experience
from core.experience_pool import ExperiencePool
from agents.engineer_with_experience import EngineerWithExperience

@pytest.fixture
def mock_experience_pool():
    pool = MagicMock(spec=ExperiencePool)
    pool.find_similar.return_value = [
        (Experience(
            question="How to load data?",
            function="def load_data(path):\n    import pandas as pd\n    return pd.read_csv(path)",
            embedding=[0.1, 0.2],
            cluster_id=0
        ), 0.95)
    ]
    return pool

@pytest.fixture
def engineer(mock_experience_pool):
    return EngineerWithExperience(mock_experience_pool)

def test_initialization(engineer, mock_experience_pool):
    assert engineer.agent_id == "engineer"
    assert engineer.experience_pool == mock_experience_pool

def test_process_invalid_input(engineer):
    message = Message("planner", "engineer", "invalid")
    response = engineer.process(message)
    assert "Invalid input" in response.content

def test_generate_code_with_experience(engineer, mock_experience_pool):
    task = Task(
        task_id="test",
        description="Test task",
        subtasks=[{"id": "1", "description": "load data"}]
    )
    message = Message("planner", "engineer", task)
    
    response = engineer.process(message)
    assert response.recipient_id == "verifier"
    
    updated_task = response.content
    assert "1" in updated_task.code_blocks
    assert "load_data" in updated_task.code_blocks["1"]
    
    mock_experience_pool.find_similar.assert_called_once()
    mock_experience_pool.add_experience.assert_called_once()

def test_fallback_to_base_implementation(engineer, mock_experience_pool):
    mock_experience_pool.find_similar.return_value = []
    
    task = Task(
        task_id="test",
        description="Test task",
        subtasks=[{"id": "1", "description": "custom task"}]
    )
    message = Message("planner", "engineer", task)
    
    response = engineer.process(message)
    assert response.recipient_id == "verifier"
    
    updated_task = response.content
    assert "1" in updated_task.code_blocks
    assert "TODO" in updated_task.code_blocks["1"]