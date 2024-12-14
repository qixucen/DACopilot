# tests/test_task.py
import pytest
from core.task import Task, TaskStatus

def test_task_initialization():
    task = Task(
        task_id="test_1",
        description="Test task",
        subtasks=[{"id": "1", "description": "subtask 1"}]
    )
    assert task.task_id == "test_1"
    assert task.status == TaskStatus.PENDING
    assert task.code_blocks is None
    assert task.execution_results is None

def test_update_status():
    task = Task("test_1", "Test task", [])
    task.update_status(TaskStatus.IN_PROGRESS)
    assert task.status == TaskStatus.IN_PROGRESS

def test_add_code_block():
    task = Task("test_1", "Test task", [])
    task.add_code_block("subtask_1", "print('hello')")
    assert "subtask_1" in task.code_blocks
    assert task.code_blocks["subtask_1"] == "print('hello')"

def test_update_execution_result():
    task = Task("test_1", "Test task", [])
    result = {"status": "success"}
    task.update_execution_result("subtask_1", result)
    assert "subtask_1" in task.execution_results
    assert task.execution_results["subtask_1"] == result