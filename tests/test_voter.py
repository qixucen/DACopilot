# tests/test_voter.py
import pytest
from agents.voter import Voter
from core.message import Message
from core.task import Task

def test_voter_initialization():
    voter = Voter(max_iterations=5)
    assert voter.agent_id == "voter"
    assert voter.max_iterations == 5
    assert voter.iterations == 0
    assert voter.candidates == []

def test_process_before_max_iterations():
    voter = Voter(max_iterations=3)
    task = Task("test", "Test task", [])
    message = Message("verifier", "voter", task)
    
    response = voter.process(message)
    assert voter.iterations == 1
    assert len(voter.candidates) == 1
    assert response.recipient_id == "planner"

def test_process_at_max_iterations():
    voter = Voter(max_iterations=2)
    task1 = Task("test1", "Test task 1", [])
    task2 = Task("test2", "Test task 2", [])
    
    # First iteration
    task1.update_execution_result("1", {"status": "success"})
    message1 = Message("verifier", "voter", task1)
    voter.process(message1)
    
    # Second iteration
    task2.update_execution_result("1", {"status": "failed"})
    message2 = Message("verifier", "voter", task2)
    response = voter.process(message2)
    
    assert voter.iterations == 2
    assert len(voter.candidates) == 2
    assert response.recipient_id == "output"
    assert response.content == task1  # Should select task1 as it has better results