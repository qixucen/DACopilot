# agents/verifier.py
from typing import Dict, Any
import traceback
from core.base_agent import BaseAgent
from core.message import Message
from core.task import Task, TaskStatus

class Verifier(BaseAgent):
    def __init__(self):
        super().__init__("verifier")
        
    def process(self, message: Message) -> Message:
        task = message.content
        if not isinstance(task, Task):
            return self.send_message("Invalid input: expected Task object", "engineer")
            
        # Execute and verify each code block
        for subtask_id, code in (task.code_blocks or {}).items():
            result = self._execute_and_verify(code)
            task.update_execution_result(subtask_id, result)
            
        if self._needs_revision(task):
            return self.send_message(task, "planner")
        return self.send_message(task, "voter")
        
    def _execute_and_verify(self, code: str) -> Dict[str, Any]:
        try:
            # Create isolated environment
            local_vars = {}
            exec(code, {}, local_vars)
            
            # Basic verification
            result = {
                "status": "success",
                "variables": list(local_vars.keys()),
                "output": str(local_vars)
            }
        except Exception as e:
            result = {
                "status": "failed",
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        return result
        
    def _needs_revision(self, task: Task) -> bool:
        """Check if any subtask failed and needs revision"""
        if not task.execution_results:
            return False
            
        return any(
            result.get("status") == "failed"
            for result in task.execution_results.values()
        )