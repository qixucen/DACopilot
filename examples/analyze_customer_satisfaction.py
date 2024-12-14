# examples/analyze_customer_satisfaction.py
from main import MultiAgentSystem
import pandas as pd

def main():
    # Define analysis requirements
    requirements = """
    Analyze customer satisfaction data from CSV:
    1. Load and validate the customer survey data
    2. Calculate basic satisfaction metrics and trends
    3. Segment customers by satisfaction level
    4. Analyze correlation between satisfaction and other variables
    5. Generate visualizations and insights report
    """

    # Initialize the multi-agent system
    system = MultiAgentSystem(max_iterations=5)
    
    # Run the analysis
    print("Starting customer satisfaction analysis...")
    result = system.run(requirements)
    
    if not result:
        print("Analysis failed!")
        return
        
    # Get the final task with generated code and results
    final_task = result.content
    
    # Print generated insights
    print("\nAnalysis Results:")
    print("-" * 50)
    
    for subtask_id, code in final_task.code_blocks.items():
        print(f"\nSubtask {subtask_id}:")
        print(code)
        
        if subtask_id in final_task.execution_results:
            result = final_task.execution_results[subtask_id]
            if result["status"] == "success":
                print("\nExecution Results:")
                print(result["output"])
            else:
                print(f"\nExecution Failed: {result['error']}")
                
    print("\nAnalysis completed successfully!")

if __name__ == "__main__":
    main()
