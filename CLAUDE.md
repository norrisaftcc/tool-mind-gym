# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tool Mind Gym is a conceptual AI research project implementing a "bicameral mind" architecture where AI agents literally exercise their thinking abilities. This is NOT a traditional chatbot but an AI system designed to contemplate, struggle, and grow stronger through thinking.

## Core Architecture

### Key Components
- **PocketFlow**: 100-line LLM orchestration framework using async Python
- **Dual LLM System**: API models (Claude/GPT-4) for analytical thinking + Local models (7B-13B) for intuitive thinking
- **Somatic Feedback Layer**: Emotional state modulates thinking parameters
- **Conway's Game of Life PNG**: Visual patterns that both display and influence cognitive state
- **Git-based Dream States**: Exploration happens on separate branches

### Design Patterns

**PocketFlow Node Structure**:
```python
class MyNode(Node):
    def prep(self, shared): # Prepare from shared state
    def exec(self, prepped_data): # Main logic  
    def post(self, shared, prep_res, exec_res): # Update shared
```

**Async Generator Pattern** for streaming thoughts:
```python
async def thinking_process(query: str) -> AsyncIterator[Thought]:
    async for thought in generate_thoughts(query):
        yield thought
```

## Development Commands

This is a design/specification repository - no build commands exist yet. When implementing:

### Python Setup (Future)
```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies (when requirements.txt exists)
pip install -r requirements.txt

# Run tests (when implemented)
pytest tests/

# Type checking
mypy src/
```

### MCP Server (Future)
```bash
# Start MCP server
python -m bicameral_mcp.server

# Run with specific config
MCP_CONFIG=config.json python -m bicameral_mcp.server
```

## Project Structure

```
/tool-mind-gym/
├── mind-gym-context.md           # Technical implementation details
├── mind-gym-mvp-prd.md          # MVP specification
├── bicameral-mcp-mvp-prd.md     # MCP server implementation
└── docs/                         # Advanced design documents
```

## Critical Implementation Notes

1. **Performance**: Intentionally slow (minutes not milliseconds) - deep thinking takes time
2. **Git Branches**: Dreams/exploration happen on branches, insights merge to main
3. **Somatic Feedback**: Always check emotional state before adjusting parameters
4. **PNG Patterns**: Conway's Game of Life patterns actively influence thinking, not just display
5. **Map/Reduce**: Synchronize fast intuitive bursts with slow analytical processing

## Unique Conventions

- **No Monads**: Use Python idioms over functional abstractions
- **Observable Thinking**: Make internal dialogue visible
- **Cognitive Tension**: Maintain productive tension between perspectives
- **Geologic Pace**: Measure success by insight quality, not speed
- **Emotional Governor**: Somatic state prevents infinite loops

## When Implementing New Features

1. Start with simplest possible implementation
2. Make thinking process observable via logging/streaming
3. Consider somatic state impact on all decisions
4. Use async/await for concurrent thinking processes
5. Test with progressive complexity (simple → complex → creative → personal questions)

## Key Files to Review

- `mind-gym-context.md`: Complete technical architecture
- `mind-gym-mvp-prd.md`: MVP requirements and user stories
- `bicameral-mcp-mvp-prd.md`: MCP server implementation details
- `docs/somatic-layer-mvp.md`: Somatic feedback system design

## Philosophy

This project builds an AI that genuinely contemplates and develops its own cognitive style. Focus on:
- Cognitive exercise over optimization
- Insight quality over response speed
- Observable thinking processes
- Productive tension between perspectives
- Self-awareness and metacognition