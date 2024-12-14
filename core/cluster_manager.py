# core/cluster_manager.py
from typing import List, Dict
import numpy as np
from sklearn.cluster import KMeans
import openai
from .experience import Experience
from .cluster_template import ClusterTemplate

class ClusterManager:
    """
    Manages clustering of experiences and template generation
    """
    def __init__(self, 
                 openai_api_key: str,
                 n_clusters: int = 10,
                 min_cluster_size: int = 3):
        self.n_clusters = n_clusters
        self.min_cluster_size = min_cluster_size
        self.kmeans = KMeans(n_clusters=n_clusters)
        openai.api_key = openai_api_key

    def cluster(self, embeddings: np.ndarray) -> np.ndarray:
        """Perform clustering on embeddings"""
        if len(embeddings) < self.n_clusters:
            # Return single cluster if not enough samples
            return np.zeros(len(embeddings), dtype=int)
            
        return self.kmeans.fit_predict(embeddings)

    def generate_template(self, experiences: List[Experience]) -> ClusterTemplate:
        """Generate template from cluster experiences"""
        if not experiences:
            raise ValueError("No experiences provided for template generation")

        # Format experiences for LLM
        prompt = self._format_template_prompt(experiences)

        try:
            # Generate template using GPT
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI that generates generalized function templates from specific examples."},
                    {"role": "user", "content": prompt}
                ]
            )

            template_text = response.choices[0].message.content
            
            # Parse template
            template_parts = template_text.split("###")
            if len(template_parts) >= 2:
                question_template = template_parts[0].strip()
                function_template = template_parts[1].strip()
            else:
                question_template = "Generic Question"
                function_template = template_text.strip()

            return ClusterTemplate(
                question_template=question_template,
                function_template=function_template,
                examples=experiences
            )

        except Exception as e:
            raise RuntimeError(f"Failed to generate template: {str(e)}")

    def _format_template_prompt(self, experiences: List[Experience]) -> str:
        """Format experiences into prompt for template generation"""
        prompt = "Generate a generalized template for these question-function pairs.\n"
        prompt += "The response should have format: QUESTION_TEMPLATE ### FUNCTION_TEMPLATE\n\n"
        
        for i, exp in enumerate(experiences, 1):
            prompt += f"Example {i}:\nQuestion: {exp.question}\nFunction:\n{exp.function}\n\n"
            
        prompt += "Generate a template that captures the common pattern in these examples."
        return prompt