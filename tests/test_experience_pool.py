# tests/test_experience_pool.py
import pytest
from unittest.mock import MagicMock
from core.experience_pool import ExperiencePool
from core.experience import Experience
from core.embedding_generator import EmbeddingGenerator
from core.vector_store import VectorStore
from core.cluster_manager import ClusterManager

@pytest.fixture
def mock_components():
    embedding_generator = MagicMock(spec=EmbeddingGenerator)
    embedding_generator.generate.return_value = [0.1, 0.2]
    
    vector_store = MagicMock(spec=VectorStore)
    vector_store.search.return_value = ([0], [0.9])
    
    cluster_manager = MagicMock(spec=ClusterManager)
    cluster_manager.cluster.return_value = [0, 1]
    
    return embedding_generator, vector_store, cluster_manager

def test_experience_pool_initialization(mock_components):
    embedding_generator, vector_store, cluster_manager = mock_components
    pool = ExperiencePool(embedding_generator, vector_store, cluster_manager)
    assert pool.experiences == []
    assert pool.templates == {}

def test_add_experience(mock_components):
    embedding_generator, vector_store, cluster_manager = mock_components
    pool = ExperiencePool(embedding_generator, vector_store, cluster_manager)
    
    exp = pool.add_experience("How to load data?", "def load_data(): pass")
    assert isinstance(exp, Experience)
    assert exp.question == "How to load data?"
    assert exp.function == "def load_data(): pass"
    assert exp.embedding == [0.1, 0.2]
    
    assert len(pool.experiences) == 1
    embedding_generator.generate.assert_called_once()
    vector_store.add_vector.assert_called_once()

def test_find_similar(mock_components):
    embedding_generator, vector_store, cluster_manager = mock_components
    pool = ExperiencePool(embedding_generator, vector_store, cluster_manager)
    
    # Add experience
    pool.add_experience("How to load data?", "def load_data(): pass")
    
    # Find similar
    similar = pool.find_similar("How to load CSV?")
    assert len(similar) == 1
    assert isinstance(similar[0][0], Experience)
    assert isinstance(similar[0][1], float)
    
    embedding_generator.generate.assert_called()
    vector_store.search.assert_called_once()

def test_update_clusters(mock_components):
    embedding_generator, vector_store, cluster_manager = mock_components
    pool = ExperiencePool(embedding_generator, vector_store, cluster_manager)
    
    # Add experiences
    pool.add_experience("How to load data?", "def load_data(): pass")
    pool.add_experience("How to save data?", "def save_data(): pass")
    
    # Update clusters
    pool.update_clusters()
    
    cluster_manager.cluster.assert_called_once()
    assert all(exp.cluster_id is not None for exp in pool.experiences)