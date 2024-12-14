# tests/test_experience.py
import pytest
import numpy as np
from core.experience import Experience

def test_experience_creation():
    exp = Experience(
        question="How to load data?",
        function="def load_data(): pass"
    )
    assert exp.question == "How to load data?"
    assert exp.function == "def load_data(): pass"
    assert exp.embedding is None
    assert exp.cluster_id is None
    assert exp.metadata == {}

def test_experience_to_dict():
    exp = Experience(
        question="How to load data?",
        function="def load_data(): pass",
        embedding=[0.1, 0.2],
        cluster_id=1,
        metadata={"type": "data_loading"}
    )
    data = exp.to_dict()
    assert data["question"] == exp.question
    assert data["function"] == exp.function
    assert data["embedding"] == exp.embedding
    assert data["cluster_id"] == exp.cluster_id
    assert data["metadata"] == exp.metadata

def test_experience_from_dict():
    data = {
        "question": "How to load data?",
        "function": "def load_data(): pass",
        "embedding": [0.1, 0.2],
        "cluster_id": 1,
        "metadata": {"type": "data_loading"}
    }
    exp = Experience.from_dict(data)
    assert exp.question == data["question"]
    assert exp.function == data["function"]
    assert exp.embedding == data["embedding"]
    assert exp.cluster_id == data["cluster_id"]
    assert exp.metadata == data["metadata"]

def test_get_embedding_array():
    exp = Experience(
        question="How to load data?",
        function="def load_data(): pass",
        embedding=[0.1, 0.2]
    )
    array = exp.get_embedding_array()
    assert isinstance(array, np.ndarray)
    assert np.allclose(array, np.array([0.1, 0.2]))

def test_get_embedding_array_none():
    exp = Experience(
        question="How to load data?",
        function="def load_data(): pass"
    )
    assert exp.get_embedding_array() is None