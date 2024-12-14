# Multi-Agent System for Automated Data Analysis

A Python-based multi-agent system that automates data analysis tasks through collaboration between specialized agents. The system breaks down complex data analysis requirements into subtasks, generates code, verifies execution, and selects optimal solutions through multiple iterations.

## System Architecture

The system consists of 4 specialized agents:

1. **Planner**: Designs data analysis workflows by breaking down requirements into concrete subtasks
2. **Engineer**: Generates Python code for each subtask based on the planner's specifications
3. **Verifier**: Executes and validates generated code, providing feedback on failures
4. **Voter**: Selects the best solution after multiple iterations (default: 5 iterations)

### Components

- **core/**
  - `base_agent.py`: Abstract base class defining agent interface
  - `message.py`: Message class for inter-agent communication
  - `task.py`: Task representation with subtasks and execution results
- **agents/**
  - `planner.py`: Analysis workflow planning
  - `engineer.py`: Code generation
  - `verifier.py`: Code execution and validation  
  - `voter.py`: Solution selection
- `main.py`: System orchestration and entry point

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/multi-agent-analysis.git
cd multi-agent-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```python
from main import MultiAgentSystem

# Define your analysis requirements
requirements = """
Analyze the customer satisfaction survey data:
1. Load the survey responses from CSV
2. Clean and preprocess the data
3. Perform statistical analysis
4. Generate visualizations
5. Identify key insights
"""

# Initialize and run the system
system = MultiAgentSystem()
result = system.run(requirements)

# Access the results
if result:
    print(f"Analysis completed: {result.content}")
```

## Development

### Adding New Capabilities

1. Extend agent capabilities by modifying their respective modules:
   - `agents/planner.py` for new analysis patterns
   - `agents/engineer.py` for code generation templates
   - `agents/verifier.py` for additional validation rules

2. Add new dependencies to `requirements.txt`

### Testing

Run tests using pytest:
```bash
python -m pytest tests/
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

2. Install dependencies:

## Usage

Example usage:


## Agent Details

### Planner
- Analyzes requirements to create structured workflow
- Breaks down complex tasks into executable subtasks
- Updates plans based on execution feedback

### Engineer
- Generates Python code for each subtask
- Supports common data analysis operations
- Updates code based on verification results

### Verifier
- Executes generated code in isolated environment
- Validates outputs and captures errors
- Provides detailed execution feedback

### Voter
- Collects solutions over multiple iterations
- Evaluates solution quality based on execution success
- Selects optimal solution using scoring system

## Development

### Adding New Features

1. Extend agent capabilities in respective agent class files
2. Update message handling in affected components
3. Add tests for new functionality
4. Update documentation

### Testing

Run tests using pytest:

### Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Create pull request

## License

MIT License

## Requirements

- Python 3.8+
- pandas >= 1.3.0
- numpy >= 1.21.0
- matplotlib >= 3.4.0
- seaborn >= 0.11.0
- pytest >= 6.2.0
