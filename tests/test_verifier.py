# tests/test_verifier.py
import pytest
from agents.verifier import Verifier
from core.message import Message
from core.task import Task

def test_verifier_initialization():
    verifier = Verifier()
    assert verifier.agent_id == "verifier"

def test_execute_valid_code():
    verifier = Verifier()
    task = Task(
        task_id="test",
        description="Test task",
        subtasks=[{"id": "1", "description": "test"}]
    )
    task.add_code_block("1", "x = 1 + 1")
    
    message = Message("engineer", "verifier", task)
    response = verifier.process(message)
    
    result = task.execution_results["1"]
    assert result["status"] == "success"
    assert "x" in result["variables"]

def test_execute_invalid_code():
    verifier = Verifier()
    task = Task(
        task_id="test",
        description="Test task",
        subtasks=[{"id": "1", "description": "test"}]
    )
    task.add_code_block("1", "invalid syntax")
    
    message = Message("engineer", "verifier", task)
    response = verifier.process(message)
    
    result = task.execution_results["1"]
    assert result["status"] == "failed"
    assert "error" in result