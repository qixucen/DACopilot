# agents/engineer.py
from typing import Dict
from core.base_agent import BaseAgent
from core.message import Message
from core.task import Task, TaskStatus

class Engineer(BaseAgent):
    def __init__(self):
        super().__init__("engineer")
        
    def process(self, message: Message) -> Message:
        task = message.content
        if not isinstance(task, Task):
            return self.send_message("Invalid input: expected Task object", "planner")
            
        # Generate or update code for pending subtasks
        updated = False
        for subtask in task.subtasks:
            if subtask["id"] not in (task.code_blocks or {}):
                code = self._generate_code(subtask)
                task.add_code_block(subtask["id"], code)
                updated = True
                
        # Always return task to verifier, even if no updates
        # This ensures the workflow continues
        return self.send_message(task, "verifier")
        
    def _generate_code(self, subtask: Dict[str, str]) -> str:
        """Generate code based on subtask description"""
        description = subtask["description"]
        
        if "load" in description.lower():
            return """
def load_and_preprocess_data(file_path):
    import pandas as pd
    data = pd.read_csv(file_path)
    # Basic preprocessing
    data = data.dropna()
    return data
"""
        elif "exploratory" in description.lower():
            return """
def perform_eda(data):
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    # Basic statistics
    summary = data.describe()
    # Correlation matrix
    corr = data.corr()
    sns.heatmap(corr)
    return summary, corr
"""
        return f"# TODO: Implement {description}"