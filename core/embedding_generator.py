# core/embedding_generator.py
from typing import List
import openai
import numpy as np

class EmbeddingGenerator:
    """
    Generates embeddings using OpenAI's API
    """
    def __init__(self, api_key: str, model: str = "text-embedding-ada-002"):
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key

    def generate(self, text: str) -> List[float]:
        """Generate embedding for input text"""
        try:
            response = openai.Embedding.create(
                model=self.model,
                input=text
            )
            return response['data'][0]['embedding']
        except Exception as e:
            raise RuntimeError(f"Failed to generate embedding: {str(e)}")

    def generate_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        try:
            response = openai.Embedding.create(
                model=self.model,
                input=texts
            )
            return [item['embedding'] for item in response['data']]
        except Exception as e:
            raise RuntimeError(f"Failed to generate embeddings: {str(e)}")

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        v1_array = np.array(v1)
        v2_array = np.array(v2)
        return float(np.dot(v1_array, v2_array) / 
                    (np.linalg.norm(v1_array) * np.linalg.norm(v2_array)))