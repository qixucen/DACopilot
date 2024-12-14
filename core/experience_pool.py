# core/experience_pool.py
import pickle
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import numpy as np
from .experience import Experience
from .embedding_generator import EmbeddingGenerator
from .vector_store import VectorStore
from .cluster_manager import ClusterManager
from .cluster_template import ClusterTemplate

class ExperiencePool:
    """
    Manages a pool of experiences with clustering and similarity search capabilities
    """
    def __init__(self, 
                 embedding_generator: EmbeddingGenerator,
                 vector_store: VectorStore,
                 cluster_manager: ClusterManager,
                 save_path: str = "experience_pool.pkl"):
        self.experiences: List[Experience] = []
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store
        self.cluster_manager = cluster_manager
        self.save_path = Path(save_path)
        self.templates: Dict[int, ClusterTemplate] = {}

    def add_experience(self, question: str, function: str) -> Experience:
        """Add new experience to the pool"""
        # Create experience
        exp = Experience(question=question, function=function)
        
        # Generate embedding
        embedding = self.embedding_generator.generate(question)
        exp.embedding = embedding
        
        # Add to experiences and vector store
        self.experiences.append(exp)
        self.vector_store.add_vector(embedding)
        
        return exp

    def update_clusters(self) -> None:
        """Update clusters and generate templates"""
        # Get all embeddings
        embeddings = [exp.get_embedding_array() for exp in self.experiences 
                     if exp.embedding is not None]
        if not embeddings:
            return

        # Perform clustering
        cluster_ids = self.cluster_manager.cluster(np.stack(embeddings))
        
        # Update experience cluster IDs
        for exp, cluster_id in zip(self.experiences, cluster_ids):
            exp.cluster_id = int(cluster_id)

        # Generate templates for each cluster
        self.templates = {}
        for cluster_id in set(cluster_ids):
            cluster_exps = [exp for exp in self.experiences 
                          if exp.cluster_id == cluster_id]
            template = self.cluster_manager.generate_template(cluster_exps)
            self.templates[cluster_id] = template

    def find_similar(self, question: str, k: int = 5) -> List[Tuple[Experience, float]]:
        """Find k most similar experiences"""
        # Generate embedding for query
        query_embedding = self.embedding_generator.generate(question)
        
        # Find similar vectors
        similar_indices, distances = self.vector_store.search(query_embedding, k)
        
        # Return experiences with similarity scores
        results = []
        for idx, dist in zip(similar_indices, distances):
            if idx < len(self.experiences):
                results.append((self.experiences[idx], float(dist)))
        return results

    def save(self) -> None:
        """Save experience pool to disk"""
        with open(self.save_path, 'wb') as f:
            pickle.dump({
                'experiences': self.experiences,
                'templates': self.templates
            }, f)

    def load(self) -> None:
        """Load experience pool from disk"""
        if not self.save_path.exists():
            return
            
        with open(self.save_path, 'rb') as f:
            data = pickle.load(f)
            self.experiences = data['experiences']
            self.templates = data.get('templates', {})
            
        # Rebuild vector store
        embeddings = [exp.embedding for exp in self.experiences 
                     if exp.embedding is not None]
        if embeddings:
            self.vector_store.rebuild(embeddings)