# core/task.py
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    task_id: str
    description: str
    subtasks: List[Dict[str, str]]
    status: TaskStatus = TaskStatus.PENDING
    code_blocks: Dict[str, str] = None
    execution_results: Dict[str, Any] = None
    
    def update_status(self, status: TaskStatus):
        self.status = status
        
    def add_code_block(self, subtask_id: str, code: str):
        if self.code_blocks is None:
            self.code_blocks = {}
        self.code_blocks[subtask_id] = code
        
    def update_execution_result(self, subtask_id: str, result: Any):
        if self.execution_results is None:
            self.execution_results = {}
        self.execution_results[subtask_id] = result