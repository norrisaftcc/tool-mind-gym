# Bicameral Agent MCP Server - MVP PRD

## Executive Summary

A minimal MCP (Model Context Protocol) server implementing a single bicameral agent using PocketFlow's graph architecture. The agent has two "hemispheres" - one running on Claude/GPT-4 (analytical) and one on a local model (intuitive) - that engage in internal dialogue before responding.

## MVP Scope

### What's In
- Single bicameral agent with two voices
- MCP server interface for tool integration
- PocketFlow graph for conversation flow
- One hemisphere on API (Anthropic/OpenAI)
- One hemisphere on local model (llama.cpp compatible)
- Basic internal dialogue loop
- Simple synthesis mechanism

### What's Out (Future Iterations)
- Multi-agent hive coordination
- Complex memory systems
- Advanced reasoning chains
- Visual debugging tools
- Agent personality customization

## Architecture

```
MCP Client (Claude Desktop, etc.)
    |
    v
MCP Server (bicameral_agent.py)
    |
    v
PocketFlow Graph
    ├── InputNode (receives query)
    ├── IntuitiveNode (local model)
    ├── AnalyticalNode (API model)
    ├── DialogueNode (internal conversation)
    └── SynthesisNode (final response)
```

## Technical Implementation

### Project Structure
```
bicameral-mcp/
├── pyproject.toml
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── server.py          # MCP server entry point
│   ├── nodes.py           # PocketFlow nodes
│   ├── flow.py            # Bicameral flow definition
│   └── utils/
│       ├── __init__.py
│       ├── call_llm.py    # LLM wrappers
│       └── local_model.py # Local model interface
└── docs/
    └── design.md
```

### Core Components

#### 1. MCP Server (`server.py`)
```python
# Minimal MCP server exposing bicameral agent as a tool
import asyncio
from pocketmcp import MCPServer
from flow import create_bicameral_flow

class BicameralMCPServer(MCPServer):
    def __init__(self):
        super().__init__("bicameral-agent")
        self.flow = create_bicameral_flow()
        
    async def think(self, query: str) -> str:
        """Bicameral thinking process"""
        shared = {
            "query": query,
            "intuitive_thoughts": [],
            "analytical_thoughts": [],
            "dialogue": [],
            "synthesis": None
        }
        
        # Run the flow
        await self.flow.run_async(shared)
        
        return shared["synthesis"]
```

#### 2. PocketFlow Nodes (`nodes.py`)
```python
from pocketflow import Node
from utils.call_llm import call_api_llm
from utils.local_model import call_local_llm

class IntuitiveNode(Node):
    """Local model for fast, intuitive responses"""
    def prep(self, shared):
        return shared["query"]
    
    def exec(self, query):
        prompt = f"""You are the intuitive hemisphere of a bicameral mind.
        Respond with immediate impressions, feelings, and associations.
        Be creative, use metaphors, trust your instincts.
        
        Query: {query}
        
        Intuitive response:"""
        
        return call_local_llm(prompt)
    
    def post(self, shared, prep_res, exec_res):
        shared["intuitive_thoughts"].append(exec_res)
        return "analytical"  # Next node

class AnalyticalNode(Node):
    """API model for deep, analytical responses"""
    def prep(self, shared):
        return {
            "query": shared["query"],
            "intuitive": shared["intuitive_thoughts"][-1]
        }
    
    def exec(self, context):
        prompt = f"""You are the analytical hemisphere of a bicameral mind.
        Analyze the query systematically, considering the intuitive response.
        Be logical, precise, and thorough.
        
        Query: {context['query']}
        
        Intuitive hemisphere said: {context['intuitive']}
        
        Analytical response:"""
        
        return call_api_llm(prompt)
    
    def post(self, shared, prep_res, exec_res):
        shared["analytical_thoughts"].append(exec_res)
        
        # Decide if more dialogue needed
        if len(shared["dialogue"]) < 2:
            return "dialogue"
        else:
            return "synthesis"

class DialogueNode(Node):
    """Internal conversation between hemispheres"""
    def prep(self, shared):
        return shared
    
    def exec(self, shared):
        # Alternate between hemispheres
        last_speaker = "analytical" if len(shared["dialogue"]) % 2 == 0 else "intuitive"
        
        if last_speaker == "analytical":
            # Intuitive responds to analytical
            prompt = f"""Continue the internal dialogue.
            Analytical said: {shared['analytical_thoughts'][-1]}
            
            Respond intuitively:"""
            response = call_local_llm(prompt)
            shared["intuitive_thoughts"].append(response)
        else:
            # Analytical responds to intuitive
            prompt = f"""Continue the internal dialogue.
            Intuitive said: {shared['intuitive_thoughts'][-1]}
            
            Respond analytically:"""
            response = call_api_llm(prompt)
            shared["analytical_thoughts"].append(response)
        
        return response
    
    def post(self, shared, prep_res, exec_res):
        shared["dialogue"].append({
            "speaker": "intuitive" if len(shared["dialogue"]) % 2 == 0 else "analytical",
            "content": exec_res
        })
        
        # Continue dialogue or synthesize
        if len(shared["dialogue"]) < 3:
            return "dialogue"
        else:
            return "synthesis"

class SynthesisNode(Node):
    """Synthesize both perspectives into unified response"""
    def prep(self, shared):
        return {
            "query": shared["query"],
            "intuitive_thoughts": shared["intuitive_thoughts"],
            "analytical_thoughts": shared["analytical_thoughts"],
            "dialogue": shared["dialogue"]
        }
    
    def exec(self, context):
        # Use API model for final synthesis
        prompt = f"""You are synthesizing a bicameral thinking process.
        
        Original query: {context['query']}
        
        Intuitive insights: {'; '.join(context['intuitive_thoughts'])}
        
        Analytical insights: {'; '.join(context['analytical_thoughts'])}
        
        Internal dialogue summary:
        {self._format_dialogue(context['dialogue'])}
        
        Synthesize these perspectives into a unified, insightful response:"""
        
        return call_api_llm(prompt)
    
    def _format_dialogue(self, dialogue):
        return '\n'.join([f"{d['speaker']}: {d['content']}" for d in dialogue])
    
    def post(self, shared, prep_res, exec_res):
        shared["synthesis"] = exec_res
        return None  # End flow
```

#### 3. Flow Definition (`flow.py`)
```python
from pocketflow import Flow
from nodes import IntuitiveNode, AnalyticalNode, DialogueNode, SynthesisNode

def create_bicameral_flow():
    # Create nodes
    intuitive = IntuitiveNode()
    analytical = AnalyticalNode()
    dialogue = DialogueNode()
    synthesis = SynthesisNode()
    
    # Define flow graph
    intuitive >> analytical
    analytical >> dialogue
    analytical >> synthesis  # Can skip to synthesis
    dialogue >> dialogue    # Self-loop for continued dialogue
    dialogue >> synthesis
    
    return Flow(start=intuitive)
```

#### 4. Local Model Wrapper (`utils/local_model.py`)
```python
import subprocess
import json

def call_local_llm(prompt: str, model_path: str = None) -> str:
    """Call local model using llama.cpp or similar"""
    if model_path is None:
        model_path = os.getenv("LOCAL_MODEL_PATH", "models/mistral-7b-instruct.gguf")
    
    # Example using llama.cpp
    cmd = [
        "llama",
        "-m", model_path,
        "-p", prompt,
        "-n", "256",
        "--temp", "0.7",
        "--top-p", "0.9"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

# Alternative: Use llama-cpp-python
from llama_cpp import Llama

class LocalModel:
    def __init__(self, model_path):
        self.llm = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_threads=8
        )
    
    def generate(self, prompt: str) -> str:
        response = self.llm(
            prompt,
            max_tokens=256,
            temperature=0.7,
            top_p=0.9
        )
        return response['choices'][0]['text']
```

## Configuration

### Environment Variables
```bash
# API Configuration
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
API_MODEL=claude-3-opus-20240229  # or gpt-4

# Local Model Configuration
LOCAL_MODEL_PATH=models/mistral-7b-instruct.gguf
LOCAL_MODEL_TYPE=llama  # or gpt4all, ollama

# Server Configuration
MCP_PORT=3000
DEBUG=true
```

### Model Selection Strategy
- **Intuitive (Local)**: Fast, creative models like Mistral 7B, Phi-2, or Llama 3 8B
- **Analytical (API)**: Powerful reasoning models like Claude 3 Opus or GPT-4

## Testing Plan

### Basic Test Flow
```python
# test_bicameral.py
async def test_basic_query():
    server = BicameralMCPServer()
    
    response = await server.think("What is consciousness?")
    
    print("=== BICAMERAL RESPONSE ===")
    print(response)
    
    # Check internal state
    print("\n=== THINKING PROCESS ===")
    print(f"Intuitive thoughts: {len(server.flow.shared['intuitive_thoughts'])}")
    print(f"Analytical thoughts: {len(server.flow.shared['analytical_thoughts'])}")
    print(f"Dialogue turns: {len(server.flow.shared['dialogue'])}")
```

### Test Queries
1. **Philosophical**: "What is the nature of reality?"
2. **Creative**: "Design a new type of musical instrument"
3. **Analytical**: "Explain the economic impacts of automation"
4. **Personal**: "How should I approach a difficult conversation?"

## Success Metrics

1. **Response Quality**: Synthesis shows both perspectives
2. **Latency**: Total response time < 30 seconds
3. **Token Efficiency**: Local model uses < 500 tokens per turn
4. **Dialogue Coherence**: Internal conversation is meaningful

## Development Timeline

### Week 1: Core Infrastructure
- Set up PocketFlow project structure
- Implement basic MCP server
- Create node implementations
- Test with mock LLMs

### Week 2: Model Integration
- Integrate local model (llama.cpp)
- Connect API model (Anthropic/OpenAI)
- Implement dialogue logic
- Test full flow

### Week 3: Polish & Deploy
- Add error handling
- Optimize prompts
- Create Docker container
- Write documentation

## Future Enhancements

1. **Memory System**: Add conversation history
2. **Multi-Agent**: Expand to agent hive
3. **Streaming**: Stream thoughts as they emerge
4. **Visualization**: Show thinking process
5. **Fine-tuning**: Optimize local model for intuitive role

## Dependencies

```toml
# pyproject.toml
[project]
name = "bicameral-mcp"
version = "0.1.0"
dependencies = [
    "pocketflow>=0.1.0",
    "anthropic>=0.18.0",
    "openai>=1.0.0",
    "llama-cpp-python>=0.2.0",
    "pocketmcp>=0.1.0",  # MCP server framework
    "asyncio",
    "python-dotenv"
]
```

## Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/bicameral-mcp
cd bicameral-mcp
pip install -e .

# Download local model
wget https://huggingface.co/mistral-7b-instruct-v0.2.Q4_K_M.gguf
mkdir models && mv *.gguf models/

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run server
python src/server.py

# Test with MCP client
mcp-client connect localhost:3000
```

This MVP provides a working bicameral agent that can be extended into a full hive system later!