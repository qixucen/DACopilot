# agents/engineer_with_experience.py
from typing import List, Optional, Tuple
from core.base_agent import BaseAgent
from core.message import Message
from core.task import Task
from core.experience import Experience
from core.experience_pool import ExperiencePool

class EngineerWithExperience(BaseAgent):
    """Engineer agent that uses experience pool for code generation"""
    
    def __init__(self, experience_pool: ExperiencePool):
        super().__init__("engineer")
        self.experience_pool = experience_pool
        
    def process(self, message: Message) -> Message:
        task = message.content
        if not isinstance(task, Task):
            return self.send_message("Invalid input: expected Task object", "planner")
            
        # Generate or update code for pending subtasks
        updated = False
        for subtask in task.subtasks:
            if subtask["id"] not in (task.code_blocks or {}):
                code = self._generate_code_with_experience(subtask)
                task.add_code_block(subtask["id"], code)
                updated = True
                
                # Add to experience pool
                self.experience_pool.add_experience(
                    question=subtask["description"],
                    function=code
                )
                
        if updated:
            return self.send_message(task, "verifier")
        return self.send_message(task, "planner")
        
    def _generate_code_with_experience(self, subtask: dict) -> str:
        """Generate code using similar experiences as examples"""
        description = subtask["description"]
        
        # Find similar experiences
        similar_experiences = self.experience_pool.find_similar(description)
        
        if not similar_experiences:
            # Fall back to simple code generation
            return self._generate_basic_code(description)
            
        # Use the most similar experience's code as template
        return self._adapt_code_from_experiences(description, similar_experiences)
        
    def _generate_basic_code(self, description: str) -> str:
        """Generate basic code template for a given description"""
        if "load" in description.lower():
            return """
def load_data(file_path):
    import pandas as pd
    return pd.read_csv(file_path)
"""
        elif "exploratory" in description.lower():
            return """
def analyze_data(data):
    import pandas as pd
    import matplotlib.pyplot as plt
    
    # Basic statistics
    stats = data.describe()
    # Plot histogram
    data.hist()
    plt.show()
    return stats
"""
        return f"# TODO: Implement {description}"
        
    def _adapt_code_from_experiences(self, 
                                   description: str, 
                                   experiences: List[Tuple[Experience, float]]) -> str:
        """Adapt code from similar experiences"""
        # Get the most similar experience
        best_match = experiences[0][0]
        
        if "load" in description.lower():
            return best_match.function
        elif "exploratory" in description.lower():
            return best_match.function
        
        return f"# TODO: Implement {description}\n{best_match.function}"