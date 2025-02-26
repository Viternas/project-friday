# Agent Prime Framework
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FViternas%2Fproject-friday&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

Agent Prime is a comprehensive, enterprise-grade framework for building intelligent agent systems with robust memory management, specialized agent capabilities, and advanced state tracking.

## 🚀 Features

- **Robust Memory Architecture**: Graph-based memory system with checkpoints and execution tracking
- **Multi-Agent Specialization**: Pre-defined specialized agents for web, data, security, and more
- **Advanced Function Normalization**: Comprehensive execution metadata capture and tracking
- **Vector-based RAG Integration**: Efficient similarity search with FAISS
- **Multi-Model Provider Support**: Seamless integration with OpenAI, OpenRouter, and Ollama
- **Checkpoint-Based Execution**: Reliable long-running task management

## 📋 Prerequisites

- Projects_utils -> https://github.com/Viternas/projects-utils
- Python 3.8+
- PostgreSQL database
- FAISS for vector operations

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/agent-prime.git
cd agent-prime

# Install dependencies
pip install -e .

# Clone the utisl lib
git clone https://github.com/Viternas/projects-utils
pip install ./projects_utils

# Set up configuration
cp config_template.json unencoded_config_main.json
# Edit unencoded_config_main.json with your API keys and settings
```

## 🔧 Configuration

The framework uses a secure configuration system. After creating your `unencoded_config_main.json` file, initialize it:

```python
from build_utils.encode_config_json import JsonFormatter
from build_utils.create_config_class import CreateConfigClass
import os

# Encode configuration
ec = JsonFormatter(
    package_dir=os.path.dirname(__file__), 
    config_file='unencoded_config_main.json', 
    encode=True
)

# Create Config class
cc = CreateConfigClass(
    package_dir=os.path.dirname(__file__), 
    config_file_name='config_main_encoded.json'
).create_config_class()
```
Example Agent Implementation Guide 

This guide demonstrates how to create an agent in the Agent Prime system using the provided ExampleAgent as reference. 
Agent Structure Overview 

The ExampleAgent follows a structured pattern: 
python
 
 
1
2
3
4
5
6
⌄
⌄
⌄
def create_example_agent():
    class ExampleAgent:
        def __init__(self, data=None):
            self.agent = data
        # Methods...
    return ExampleAgent
 
 
Key Components 
1. Function Mapping 

Agents provide function maps to expose available operations: 
python
 
 
1
2
3
4
5
6
7
8
9
10
⌄
⌄
⌄
⌄
def _map_function(self):
    return {
        'EXAMPLE_FUNCTION': self.example_function,
    }

@staticmethod
def _map_arguments():
    return {
        'EXAMPLE_FUNCTION': 'example_function_basemodel',
    }
 
 
2. Function Execution 

The _run_function method handles executing mapped functions: 
python
 
 
1
2
⌄
def _run_function(self, handler, args_dict, context):
    return handler(**args_dict)
 
 
3. Memory-Augmented Functions 

Functions use decorators for memory tracking and normalization: 
python
 
 
1
2
3
4
5
⌄
@self.agent.memory.add_to_memory_decorator()
@self.agent.memory.function_normalizer.normalize()
@self.agent.memory.function_type_label(FunctionType.DATA_PROCESSING.value)
def _example_function_processing(*args, **kwargs):
    return 5
 
 

These decorators: 

     Add function execution to agent memory
     Normalize function output for consistent handling
     Label the function with its type (REASONING, DATA_PROCESSING, etc.)
     

4. Function Types 

Functions can be categorized with FunctionType enum: 

     REASONING: For logic and reasoning operations
     DATA_PROCESSING: For data manipulation operations
     PROCESSED_DATA: For operations producing final data
     

5. Multi-Step Processing 

Complex operations can be split into multiple steps: 
python
 
 
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
⌄
⌄
⌄
⌄
def example_function(self, checkpoint_uuid, step_uuid, previous_step_uuid, function_arguments):
    # Step 1: Processing
    @decorators...
    def _example_function_processing(*args, **kwargs):
        return 5
        
    # Step 2: Thinking
    @decorators...
    def _example_function_thinking(*args, **kwargs):
        return 50
        
    # Execution function
    def _run_test_function(*args, **kwargs):
        # Execute step 1
        _example_function_processing(...)
        
        # Execute step 2 with new step_uuid
        _example_function_thinking(
            checkpoint_uuid=checkpoint_uuid,
            step_uuid=str(uuid4()),  # New UUID for this step
            previous_step_uuid=step_uuid,  # Link to previous step
            function_arguments=function_arguments
        )
 
 
Core Agent Functions 
Single Function Call 

Handles executing single function calls: 
python
 
 
1
2
3
4
5
6
7
8
9
10
11
12
13
14
⌄
⌄
def single_function_call(self, checkpoint_uuid, step_uuid, previous_step_uuid, function_arguments):
    @decorators...
    def _single_function_call(*args, **kwargs):
        # Get parameters from function_arguments
        self.agent.thinking.task = function_arguments.get('checkpoint')
        previous_function = function_arguments.get('previous_function')
        previous_function_output = function_arguments.get('previous_function_output')
        task = function_arguments.get('task')
        
        # Execute thinking function and capture result and cost
        single_function_call, cost = self.agent.thinking.single_function_call(
            replacement_items=[previous_function, previous_function_output, task]
        )
        return single_function_call, cost
 
 
Arguments Builder 

Prepares arguments for function execution: 
python
 
 
1
2
3
4
5
6
7
8
⌄
⌄
def arguments_for_single_function_call(self, checkpoint_uuid, step_uuid, previous_step_uuid, function_arguments):
    @decorators...
    def _arguments_for_single_function_call(*args, **kwargs):
        # Similar to single_function_call but for argument preparation
        map_to_args, cost = self.agent.thinking.arguments_for_single_function_call(
            replacement_items=[previous_function, previous_function_output, task]
        )
        return map_to_args, cost
 
 
Creating Your Own Agent 

     Create a function that returns your agent class
     Implement required methods: run(), _map_function(), _map_arguments(), _run_function()
     Add your specialized functions with proper decorators
     Register your agent in the agent registry
     Call it through Agent Prime
     

Each agent operation should be tracked with memory decorators to build the knowledge graph and maintain execution history. 


## 🚀 Quick Start

```python
from agent_prime.agent_prime import AgentPrime

```
# Initialize the agent system
agent = AgentPrime()
agent.initialise_class_runtimes()

# Register with orchestration layer and get task assignments
agent.initialise_agent_uuids()

if agent.work_available:
    # Get task information
    agent.get_task_information()
    
    # Initialize checkpoint system
    if not agent.check_for_existing_checkpoints():
        agent.generate_checkpoints()
    
    # Initialize memory system
    agent.initialise_memory_system()
    
    # Run specialized agent based on task requirements
    agent.initialise_agent_polymorphism()
```

## 🏗️ Architecture

### Core Components

#### AgentMemory
The memory subsystem tracks execution steps, manages checkpoints, and enables retrieval of past operations.

```python
from agent_memory.agent_internal_memory import AgentMemory

memory = AgentMemory(ai_driver=ai_driver)
memory.map_checkpoint_to_dataclass()
memory.build_graph_initial_from_checkpoint_dataclass_list()
```

#### Function Normalization
The framework captures comprehensive metadata for every function execution:

```python
@memory.function_normalizer.normalize()
@memory.function_type_label(FunctionType.REASONING.value)
def example_function(*args, **kwargs):
    # Function implementation
    return result
```

#### HashRAG
Vector-based retrieval system for efficient information retrieval:

```python
from agent_memory.hash_rag.HashRag import HashRag

rag = HashRag(ai_driver=ai_driver)
results = rag.search(query="What steps did we take to analyze the data?", k=3)
```

#### Specialized Agents
The framework provides specialized agents for different domains:

- `ExampleAgent`: Basic agent implementation
- `WebAgent`: Web interactions and scraping
- `DataAgent`: Data analysis and processing
- `SecurityAgent`: Security analysis
- `BusinessAgent`: Business logic
- And more...

## 🌐 Advanced Usage

### Creating Custom Agent

```python
def create_custom_agent():
    class CustomAgent:
        def __init__(self, data=None):
            self.agent = data
            
        def run(self):
            # Custom implementation
            pass
            
        def _map_function(self):
            return {
                'CUSTOM_FUNCTION': self.custom_function,
            }
            
        def custom_function(self, checkpoint_uuid, step_uuid, previous_step_uuid, function_arguments):
            # Function implementation with memory integration
            pass
            
    return CustomAgent()
```

### Working with the Graph Memory System

```python
# Add execution steps to memory
from uuid import uuid4

step_uuid = str(uuid4())
memory.add_steps_to_memory(
    normalised_output=function_output, 
    checkpoint_uuid=checkpoint_uuid, 
    step_uuid=step_uuid
)

# Query graph for execution paths
parallel_paths = memory.graph_memory.get_parallel_execution_paths()
critical_path = memory.graph_memory.get_critical_path()
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- OpenAI, Anthropic, and other LLM providers
- FAISS library for vector search
- The open source AI agent community


