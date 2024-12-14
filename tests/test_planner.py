# tests/test_planner.py
import pytest
from agents.planner import Planner
from core.message import Message
from core.task import Task, TaskStatus

def test_planner_initialization():
    planner = Planner()
    assert planner.agent_id == "planner"

def test_create_analysis_plan():
    planner = Planner()
    message = Message("user", "planner", "Analyze customer data")
    response = planner.process(message)
    
    assert response.recipient_id == "engineer"
    task = response.content
    assert task.description == "Analyze customer data"
    assert len(task.subtasks) > 0
    assert all(isinstance(st, dict) for st in task.subtasks)

def test_update_plan():
    planner = Planner()
    # Create initial plan
    init_message = Message("user", "planner", "Test analysis")
    task = planner.process(init_message).content
    
    # Add failed execution result
    task.update_execution_result("1", {"status": "failed"})
    
    # Update plan
    update_message = Message("verifier", "planner", task)
    updated_task = planner.process(update_message).content
    
    assert updated_task is not None
    assert isinstance(updated_task, Task)