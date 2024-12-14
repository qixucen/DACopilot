# examples/analyze_data_with_experience.py
import os
from main import MultiAgentSystem
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_with_experience():
    """Example usage of the multi-agent system with experience pool"""
    
    # Get OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    # Initialize system with custom experience pool path
    system = MultiAgentSystem(
        openai_api_key=api_key,
        experience_pool_path="custom_experience_pool.pkl"
    )
    
    # Define analysis tasks
    tasks = [
        # Task 1: Basic data analysis
        """
        Analyze sales data:
        1. Load monthly sales data from CSV
        2. Calculate basic statistics
        3. Plot trends
        4. Generate summary report
        """,
        
        # Task 2: Customer segmentation
        """
        Perform customer segmentation:
        1. Load customer transaction data
        2. Clean and normalize features
        3. Apply clustering algorithms
        4. Visualize segments
        5. Generate segment profiles
        """,
        
        # Task 3: Sentiment analysis
        """
        Analyze customer feedback:
        1. Load customer reviews
        2. Preprocess text data
        3. Perform sentiment analysis
        4. Identify common themes
        5. Generate insights report
        """
    ]
    
    # Run analysis for each task
    for i, requirements in enumerate(tasks, 1):
        logger.info(f"\nExecuting Task {i}...")
        logger.info(f"Requirements:\n{requirements}")
        
        result = system.run(requirements)
        
        if result and result.content:
            task = result.content
            logger.info("\nGenerated Code Blocks:")
            for subtask_id, code in task.code_blocks.items():
                logger.info(f"\nSubtask {subtask_id}:")
                logger.info(code)
                
            if task.execution_results:
                logger.info("\nExecution Results:")
                for subtask_id, result in task.execution_results.items():
                    logger.info(f"\nSubtask {subtask_id}: {result}")
        else:
            logger.error(f"Task {i} failed to produce results")
            
    logger.info("\nAll tasks completed. Experience pool updated and saved.")

if __name__ == "__main__":
    analyze_with_experience()