# tests/test_embedding_generator.py
import pytest
from unittest.mock import patch, MagicMock
import numpy as np
from core.embedding_generator import EmbeddingGenerator

@pytest.fixture
def embedding_generator():
    return EmbeddingGenerator("fake-api-key")

def test_generate(embedding_generator):
    with patch('openai.Embedding.create') as mock_create:
        mock_create.return_value = {
            'data': [{'embedding': [0.1, 0.2, 0.3]}]
        }
        
        embedding = embedding_generator.generate("test text")
        assert embedding == [0.1, 0.2, 0.3]
        
        mock_create.assert_called_once_with(
            model="text-embedding-ada-002",
            input="test text"
        )

def test_generate_batch(embedding_generator):
    with patch('openai.Embedding.create') as mock_create:
        mock_create.return_value = {
            'data': [
                {'embedding': [0.1, 0.2]},
                {'embedding': [0.3, 0.4]}
            ]
        }
        
        embeddings = embedding_generator.generate_batch(["text1", "text2"])
        assert embeddings == [[0.1, 0.2], [0.3, 0.4]]
        
        mock_create.assert_called_once_with(
            model="text-embedding-ada-002",
            input=["text1", "text2"]
        )

def test_cosine_similarity():
    v1 = [1.0, 0.0]
    v2 = [1.0, 0.0]
    v3 = [0.0, 1.0]
    
    sim1 = EmbeddingGenerator.cosine_similarity(v1, v2)
    sim2 = EmbeddingGenerator.cosine_similarity(v1, v3)
    
    assert pytest.approx(sim1) == 1.0
    assert pytest.approx(sim2) == 0.0

def test_generate_error(embedding_generator):
    with patch('openai.Embedding.create') as mock_create:
        mock_create.side_effect = Exception("API Error")
        
        with pytest.raises(RuntimeError):
            embedding_generator.generate("test text")