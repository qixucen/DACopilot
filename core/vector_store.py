# core/vector_store.py
from typing import List, Tuple
import numpy as np
from sklearn.neighbors import NearestNeighbors

class VectorStore:
    """
    Stores and searches vector embeddings
    """
    def __init__(self, metric: str = 'cosine'):
        self.metric = metric
        self.nn = NearestNeighbors(metric=metric)
        self.vectors = None

    def add_vector(self, vector: List[float]) -> None:
        """Add a new vector to the store"""
        vector_array = np.array(vector).reshape(1, -1)
        if self.vectors is None:
            self.vectors = vector_array
        else:
            self.vectors = np.vstack([self.vectors, vector_array])
        self._fit()

    def add_vectors(self, vectors: List[List[float]]) -> None:
        """Add multiple vectors to the store"""
        vectors_array = np.array(vectors)
        if self.vectors is None:
            self.vectors = vectors_array
        else:
            self.vectors = np.vstack([self.vectors, vectors_array])
        self._fit()

    def rebuild(self, vectors: List[List[float]]) -> None:
        """Rebuild the vector store with new vectors"""
        self.vectors = np.array(vectors)
        self._fit()

    def search(self, query: List[float], k: int = 5) -> Tuple[List[int], List[float]]:
        """Find k nearest neighbors"""
        if self.vectors is None or len(self.vectors) == 0:
            return [], []
            
        query_array = np.array(query).reshape(1, -1)
        distances, indices = self.nn.kneighbors(
            query_array, 
            n_neighbors=min(k, len(self.vectors))
        )
        return indices[0].tolist(), distances[0].tolist()

    def _fit(self) -> None:
        """Fit the nearest neighbors model"""
        if self.vectors is not None and len(self.vectors) > 0:
            self.nn.fit(self.vectors)