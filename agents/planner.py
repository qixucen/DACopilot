# agents/planner.py
from typing import List, Dict
import uuid
from core.base_agent import BaseAgent
from core.message import Message
from core.task import Task, TaskStatus

class Planner(BaseAgent):
    def __init__(self):
        super().__init__("planner")
        
    def process(self, message: Message) -> Message:
        if isinstance(message.content, str):
            # Create new analysis plan
            task = self._create_analysis_plan(message.content)
            return self.send_message(task, "engineer")
        elif isinstance(message.content, Task):
            # Update existing plan based on feedback
            updated_task = self._update_plan(message.content)
            return self.send_message(updated_task, "engineer")
            
    def _create_analysis_plan(self, requirements: str) -> Task:
        # Validate requirements
        if not requirements or not isinstance(requirements, str):
            raise ValueError("Invalid requirements: must be a non-empty string")
            
        # Check for basic structure
        if ";;;" in requirements or ":::" in requirements:
            raise ValueError(f"Invalid requirements format: {requirements}")
            
        # Break down requirements into subtasks
        subtasks = self._generate_subtasks(requirements)
        
        return Task(
            task_id=str(uuid.uuid4()),
            description=requirements,
            subtasks=subtasks
        )
        
    def _update_plan(self, task: Task) -> Task:
        # Analyze execution results and modify plan if needed
        if task.execution_results:
            for subtask_id, result in task.execution_results.items():
                if result.get("status") == "failed":
                    # Modify failed subtask
                    self._modify_subtask(task, subtask_id)
        return task

    def _modify_subtask(self, task: Task, failed_subtask_id: str):
        """Modify a failed subtask by breaking it down or simplifying it"""
        # Find the failed subtask
        failed_subtask = next(
            (st for st in task.subtasks if st["id"] == failed_subtask_id),
            None
        )
        
        if not failed_subtask:
            return
            
        # Break down the failed task into smaller steps
        description = failed_subtask["description"]
        if "data" in description.lower():
            # Break down data processing task
            new_subtasks = [
                {"id": f"{failed_subtask_id}_1", "description": "Import required libraries and validate data format"},
                {"id": f"{failed_subtask_id}_2", "description": "Handle missing values and outliers"},
                {"id": f"{failed_subtask_id}_3", "description": "Transform data into required format"}
            ]
        elif "analysis" in description.lower():
            # Break down analysis task
            new_subtasks = [
                {"id": f"{failed_subtask_id}_1", "description": "Calculate basic statistics"},
                {"id": f"{failed_subtask_id}_2", "description": "Perform detailed analysis"},
                {"id": f"{failed_subtask_id}_3", "description": "Summarize findings"}
            ]
        else:
            # Generic breakdown
            new_subtasks = [
                {"id": f"{failed_subtask_id}_1", "description": f"Initial step: {description}"},
                {"id": f"{failed_subtask_id}_2", "description": f"Verify and validate results"}
            ]
            
        # Replace the failed subtask with new subtasks
        task.subtasks = [
            st for st in task.subtasks if st["id"] != failed_subtask_id
        ] + new_subtasks
        
    def _generate_subtasks(self, requirements: str) -> List[Dict[str, str]]:
        # Example subtasks generation
        subtasks = [
            {"id": "1", "description": "Load and preprocess data"},
            {"id": "2", "description": "Perform exploratory data analysis"},
            {"id": "3", "description": "Build analytical models"},
            {"id": "4", "description": "Generate insights and visualizations"}
        ]
        return subtasks