# tests/test_vector_store.py
import pytest
import numpy as np
from core.vector_store import VectorStore

@pytest.fixture
def vector_store():
    return VectorStore()

def test_add_vector(vector_store):
    vector = [1.0, 0.0, 0.0]
    vector_store.add_vector(vector)
    assert vector_store.vectors is not None
    assert vector_store.vectors.shape == (1, 3)
    assert np.allclose(vector_store.vectors[0], vector)

def test_add_vectors(vector_store):
    vectors = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0]
    ]
    vector_store.add_vectors(vectors)
    assert vector_store.vectors.shape == (2, 3)
    assert np.allclose(vector_store.vectors, vectors)

def test_rebuild(vector_store):
    # Add initial vectors
    vector_store.add_vector([1.0, 0.0])
    
    # Rebuild with new vectors
    new_vectors = [[0.0, 1.0], [1.0, 1.0]]
    vector_store.rebuild(new_vectors)
    
    assert vector_store.vectors.shape == (2, 2)
    assert np.allclose(vector_store.vectors, new_vectors)

def test_search(vector_store):
    vectors = [
        [1.0, 0.0, 0.0],  # Vector 0
        [0.0, 1.0, 0.0],  # Vector 1
        [0.0, 0.0, 1.0]   # Vector 2
    ]
    vector_store.add_vectors(vectors)
    
    # Search for most similar to [1.0, 0.0, 0.0]
    indices, distances = vector_store.search([1.0, 0.0, 0.0], k=2)
    
    assert len(indices) == 2
    assert len(distances) == 2
    assert indices[0] == 0  # Most similar should be vector 0

def test_search_empty_store(vector_store):
    indices, distances = vector_store.search([1.0, 0.0], k=5)
    assert indices == []
    assert distances == []