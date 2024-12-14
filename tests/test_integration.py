# tests/test_integration.py
import pytest
from unittest.mock import patch
from main import MultiAgentSystem
from core.task import Task, TaskStatus
from core.experience import Experience

@pytest.fixture
def mock_openai_api_key():
    return "test-api-key-12345"

def test_system_initialization(mock_openai_api_key):
    system = MultiAgentSystem(openai_api_key=mock_openai_api_key)
    assert len(system.agents) == 4
    assert all(agent_id in system.agents for agent_id in ["planner", "engineer", "verifier", "voter"])

def test_complete_analysis_workflow(mock_openai_api_key):
    system = MultiAgentSystem(
        openai_api_key=mock_openai_api_key,
        max_iterations=2
    )
    requirements = """
    Simple data analysis:
    1. Calculate mean and median
    2. Generate histogram
    """
    
    with patch('openai.Embedding.create') as mock_embedding:
        mock_embedding.return_value = {'data': [{'embedding': [0.1, 0.2]}]}
        result = system.run(requirements)
        
    assert result is not None
    assert result.recipient_id == "output"
    
    final_task = result.content
    assert final_task.status != TaskStatus.FAILED
    assert final_task.code_blocks is not None
    assert final_task.execution_results is not None

def test_system_error_handling(mock_openai_api_key):
    system = MultiAgentSystem(openai_api_key=mock_openai_api_key)
    with patch('openai.Embedding.create') as mock_embedding:
        mock_embedding.side_effect = Exception("API Error")
        result = system.run("invalid:::syntax;;requirements")
        
    assert result is not None  # System should not crash
    assert result.recipient_id == "output"
    
    task = result.content
    assert isinstance(task, Task)
    assert task.status == TaskStatus.FAILED