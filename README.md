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

## 🚀 Quick Start

```python
from agent_prime.agent_prime import AgentPrime

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


