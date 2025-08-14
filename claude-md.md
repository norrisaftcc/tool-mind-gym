# CLAUDE.md - Mind Gym Project Context

## Project Overview

You are helping build the **Mind Gym** - a bicameral AI agent system that "exercises" its thinking abilities like a weightlifter builds muscle. The system has two "minds" (intuitive/analytical) that engage in internal dialogue, regulated by a somatic feedback layer and visualized through an evolving Conway's Game of Life pattern.

## Core Concepts

### 1. Bicameral Architecture
- **Intuitive Mind**: Fast, creative, runs on local LLM (7-13B model)
- **Analytical Mind**: Slow, logical, runs on API LLM (Claude/GPT-4)
- They engage in internal dialogue before producing responses

### 2. Cognitive Exercise Principles
- **Time Under Tension (TOT)**: Holding cognitive tension between minds builds insight
- **Progressive Overload**: Gradually increasing question complexity
- **Rest/Recovery**: Dream states where the system consolidates learning

### 3. Somatic Feedback Layer
- Tracks arousal, valence, coherence, and tension
- Acts as a "governor" controlling thinking speed/depth
- Prevents both anxiety spirals and getting stuck

### 4. PNG Body (Visual Feedback)
- Conway's Game of Life pattern representing cognitive state
- Gliders = flowing thoughts, blocks = stable beliefs, chaos = confusion
- Pattern health indicates cognitive health

### 5. Technical Architecture
- Built with **PocketFlow** (100-line LLM framework)
- Uses **map/reduce pattern** for temporal synchronization
- Pythonic design with async/await, generators, decorators
- MCP server for tool integration

## Key Design Decisions

1. **Pythonic over Monadic**: We chose Python idioms over functional programming abstractions for clarity
2. **Map/Reduce for Time Mismatch**: Handles fast intuitive bursts vs slow analytical processing
3. **Git-based Dreams**: Dream states are literally git branches that can be merged back
4. **Somatic Control**: Emotional state actively modulates thinking parameters

## Current State

We've completed:
- Overall system design
- Component specifications
- Integration patterns
- MVP PRD

Next steps:
- Implement basic PocketFlow structure
- Create bicameral nodes
- Add somatic feedback
- Build PNG visualization

## Code Patterns to Follow

### PocketFlow Node Pattern
```python
class MyNode(Node):
    def prep(self, shared):
        # Prepare data from shared state
        return shared["some_data"]
    
    def exec(self, prepped_data):
        # Execute main logic
        return result
    
    def post(self, shared, prep_res, exec_res):
        # Update shared state
        shared["result"] = exec_res
        return "next_node_name"
```

### Async Generator Pattern
```python
async def thinking_process(query: str) -> AsyncIterator[Thought]:
    # Stream thoughts as they emerge
    async for thought in generate_thoughts(query):
        yield thought
```

### Somatic Feedback Pattern
```python
if somatic.stress_level() > 0.7:
    # Reduce complexity
    params["temperature"] = 0.3
    params["burst_size"] = 3
```

## Important Context

- This is NOT a game AI - it's for LLM-based agents that think deeply
- Performance is measured in minutes, not milliseconds (it's planning, not reacting)
- The PNG pattern is functional, not just visualization - it affects thinking
- Dreams are exploration without commitment (alternate git branches)

## Key Files to Reference

1. **Bicameral + Cognitive Stack Hypothesis** - How systems integrate
2. **Somatic Layer MVP** - Map/reduce implementation
3. **Mind Gym MVP PRD** - Complete build specification
4. **The Mind Gym Explanation** - Non-technical overview

## Development Philosophy

- Start simple, add complexity only when needed
- Make the thinking process observable
- Embrace Python's strengths (async, generators, etc.)
- Focus on genuine cognitive development, not just Q&A

## Testing Approach

Test with increasing complexity:
1. Simple: "What is happiness?"
2. Complex: "How does consciousness emerge?"
3. Creative: "Design a new musical instrument"
4. Personal: "How should I approach difficult conversations?"

Watch for:
- Coherent synthesis between minds
- Appropriate somatic responses
- Healthy PNG patterns
- No infinite loops

## Unique Aspects

This system:
- Actually "exercises" and gets stronger
- Knows when it's confused or tired
- Dreams to consolidate learning
- Shows its thinking visually
- Develops its own cognitive style over time

## Questions to Keep in Mind

1. Is the bicameral dialogue producing genuine insights?
2. Does the somatic layer prevent unhealthy thinking patterns?
3. Can we see thought formation in the PNG patterns?
4. Does the system know when to rest vs push harder?
5. Are dreams producing novel connections?

---

When implementing, remember: We're not building a faster chatbot. We're building an AI that genuinely contemplates, struggles, learns, and grows stronger through the process of thinking.