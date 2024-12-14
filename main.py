# main.py
import os
import logging
from typing import Dict, Optional
from core.base_agent import BaseAgent
from core.message import Message
from core.task import Task, TaskStatus
from core.experience_pool import ExperiencePool
from core.embedding_generator import EmbeddingGenerator
from core.vector_store import VectorStore
from core.cluster_manager import ClusterManager
from agents.planner import Planner
from agents.engineer_with_experience import EngineerWithExperience
from agents.verifier import Verifier
from agents.voter import Voter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiAgentSystem:
    def __init__(self, 
                 openai_api_key: str,
                 max_iterations: int = 5,
                 experience_pool_path: str = "experience_pool.pkl"):
        # Initialize experience pool components
        embedding_generator = EmbeddingGenerator(openai_api_key)
        vector_store = VectorStore()
        cluster_manager = ClusterManager(openai_api_key)
        
        # Create experience pool
        self.experience_pool = ExperiencePool(
            embedding_generator=embedding_generator,
            vector_store=vector_store,
            cluster_manager=cluster_manager,
            save_path=experience_pool_path
        )
        
        # Load existing experiences
        self.experience_pool.load()
        
        # Initialize agents
        self.agents: Dict[str, BaseAgent] = {
            "planner": Planner(),
            "engineer": EngineerWithExperience(self.experience_pool),
            "verifier": Verifier(),
            "voter": Voter(max_iterations)
        }
        
    def run(self, requirements: str) -> Optional[Message]:
        """Run the multi-agent system with given requirements"""
        try:
            current_message = Message(
                sender_id="input",
                recipient_id="planner",
                content=requirements
            )
            
            while True:
                if current_message.recipient_id == "output":
                    logger.info("Analysis completed successfully")
                    # Update clusters periodically
                    self.experience_pool.update_clusters()
                    self.experience_pool.save()
                    return current_message
                    
                agent = self.agents.get(current_message.recipient_id)
                if not agent:
                    logger.error(f"Unknown agent: {current_message.recipient_id}")
                    break
                    
                logger.info(f"Processing message: {current_message}")
                next_message = agent.process(current_message)
                
                if not next_message:
                    logger.error(f"Agent {current_message.recipient_id} failed to produce response")
                    if current_message.recipient_id in ["engineer", "verifier"]:
                        next_message = Message(
                            sender_id=current_message.recipient_id,
                            recipient_id="planner",
                            content=current_message.content
                        )
                    else:
                        break
                
                current_message = next_message
                
        except Exception as e:
            logger.error(f"System error: {str(e)}")
            error_task = Task(
                task_id="error",
                description=str(e),
                subtasks=[]
            )
            error_task.update_status(TaskStatus.FAILED)
            return Message(
                sender_id="system",
                recipient_id="output",
                content=error_task
            )
            
        return None

def main():
    # Get OpenAI API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
        
    # Initialize system
    system = MultiAgentSystem(api_key)
    
    # Example usage
    requirements = """
    Analyze the customer satisfaction survey data:
    1. Load the survey responses from CSV
    2. Clean and preprocess the data
    3. Perform statistical analysis
    4. Generate visualizations
    5. Identify key insights
    """
    
    result = system.run(requirements)
    
    if result:
        logger.info(f"Final result: {result.content}")
    else:
        logger.error("System failed to produce result")

if __name__ == "__main__":
    main()