# tests/test_cluster_manager.py
import pytest
from unittest.mock import patch, MagicMock
import numpy as np
from core.cluster_manager import ClusterManager
from core.experience import Experience
from core.cluster_template import ClusterTemplate

@pytest.fixture
def cluster_manager():
    return ClusterManager("fake-api-key", n_clusters=2)

def test_cluster(cluster_manager):
    embeddings = np.array([
        [1.0, 0.0],
        [0.9, 0.1],
        [0.0, 1.0],
        [0.1, 0.9]
    ])
    
    cluster_ids = cluster_manager.cluster(embeddings)
    assert len(cluster_ids) == 4
    assert len(set(cluster_ids)) <= 2  # Should have at most 2 clusters

def test_cluster_small_dataset(cluster_manager):
    embeddings = np.array([[1.0, 0.0]])
    cluster_ids = cluster_manager.cluster(embeddings)
    assert len(cluster_ids) == 1
    assert cluster_ids[0] == 0

def test_generate_template(cluster_manager):
    experiences = [
        Experience("How to load CSV?", "def load_csv(): pass"),
        Experience("How to load Excel?", "def load_excel(): pass")
    ]
    
    with patch('openai.ChatCompletion.create') as mock_create:
        mock_create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(
                content="Load Data Template ### def load_file(path: str): pass"
            ))]
        )
        
        template = cluster_manager.generate_template(experiences)
        assert isinstance(template, ClusterTemplate)
        assert template.question_template == "Load Data Template"
        assert template.function_template == "def load_file(path: str): pass"
        assert template.examples == experiences

def test_generate_template_no_experiences(cluster_manager):
    with pytest.raises(ValueError):
        cluster_manager.generate_template([])

def test_generate_template_api_error(cluster_manager):
    experiences = [
        Experience("How to load CSV?", "def load_csv(): pass")
    ]
    
    with patch('openai.ChatCompletion.create') as mock_create:
        mock_create.side_effect = Exception("API Error")
        
        with pytest.raises(RuntimeError):
            cluster_manager.generate_template(experiences)