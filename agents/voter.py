# agents/voter.py
from typing import List, Optional
from core.base_agent import BaseAgent
from core.message import Message
from core.task import Task, TaskStatus

class Voter(BaseAgent):
    def __init__(self, max_iterations: int = 5):
        super().__init__("voter")
        self.max_iterations = max_iterations
        self.iterations = 0
        self.candidates: List[Task] = []
        
    def process(self, message: Message) -> Optional[Message]:
        task = message.content
        if not isinstance(task, Task):
            return self.send_message("Invalid input: expected Task object", "verifier")
            
        self.candidates.append(task)
        self.iterations += 1
        
        if self.iterations >= self.max_iterations:
            best_task = self._select_best_task()
            return self.send_message(best_task, "output")
        return self.send_message(task, "planner")
        
    def _select_best_task(self) -> Task:
        """Select the best task based on execution results"""
        def score_task(task: Task) -> float:
            if not task.execution_results:
                return 0.0
                
            success_rate = sum(
                1 for result in task.execution_results.values()
                if result.get("status") == "success"
            ) / len(task.execution_results)
            
            return success_rate
            
        scored_tasks = [(score_task(task), task) for task in self.candidates]
        return max(scored_tasks, key=lambda x: x[0])[1]