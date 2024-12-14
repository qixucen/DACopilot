# tests/test_engineer.py
import pytest
from agents.engineer import Engineer
from core.message import Message
from core.task import Task

def test_engineer_initialization():
    engineer = Engineer()
    assert engineer.agent_id == "engineer"

def test_process_invalid_input():
    engineer = Engineer()
    message = Message("planner", "engineer", "invalid")
    response = engineer.process(message)
    assert "Invalid input" in response.content

def test_generate_code():
    engineer = Engineer()
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
    assert "load_and_preprocess_data" in updated_task.code_blocks["1"]