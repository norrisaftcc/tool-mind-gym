# Mind Gym MVP - Product Requirements Document

## Executive Summary

Build a minimal "Mind Gym" - a bicameral AI agent with cognitive exercise capabilities, implemented as an MCP server using PocketFlow and Pythonic patterns. The MVP demonstrates core concepts: two-minded dialogue, somatic feedback, visual "body" patterns, and basic cognitive workouts.

## MVP Goals

1. **Prove the bicameral architecture works** with real LLMs
2. **Demonstrate cognitive "exercise"** through sustained dialogue
3. **Show visual feedback** via evolving PNG patterns
4. **Validate somatic layer** as a control mechanism
5. **Test with real users** asking philosophical questions

## Technical Stack

- **Framework**: PocketFlow (100-line LLM framework)
- **Language**: Python 3.11+ with async/await
- **API LLM**: Anthropic Claude or OpenAI GPT-4
- **Local LLM**: Llama.cpp with 7B-13B model
- **Visualization**: PIL/Pillow for PNG generation
- **Server**: MCP (Model Context Protocol)
- **State Storage**: Git for dream branches

## Core Components

### 1. Bicameral Engine

```python
# src/bicameral_engine.py
from pocketflow import Flow, Node
import asyncio
from typing import AsyncIterator

class BicameralFlow:
    """Main thinking engine with map/reduce pattern"""
    
    def __init__(self, api_model="claude-3-opus", local_model_path="./models/mistral-7b.gguf"):
        self.flow = self._build_flow()
        self.api_model = api_model
        self.local_model = LocalLLM(local_model_path)
        
    def _build_flow(self):
        # Nodes
        intuitive_map = IntuitiveMapNode()      # Fast bursts
        somatic_reduce = SomaticReduceNode()    # Filter by feeling
        analytical_map = AnalyticalMapNode()    # Deep analysis
        dialogue = DialogueNode()               # Internal conversation
        synthesis = SynthesisNode()             # Final integration
        
        # Flow
        intuitive_map >> somatic_reduce >> analytical_map >> dialogue >> synthesis
        dialogue >> dialogue  # Self-loop for extended conversation
        
        return Flow(start=intuitive_map)
    
    async def think(self, query: str, max_tension_time: float = 30.0) -> AsyncIterator[dict]:
        """Generate thoughts with time under tension"""
        shared = {
            "query": query,
            "somatic": SomaticState(),
            "png_state": PNGBody(),
            "tension_start": time.time(),
            "max_tension": max_tension_time
        }
        
        # Stream thoughts as they emerge
        async for thought in self.flow.run_async_generator(shared):
            yield thought
```

### 2. Somatic Layer

```python
# src/somatic.py
from dataclasses import dataclass
import numpy as np

@dataclass
class SomaticState:
    """Minimal emotional/body state"""
    arousal: float = 0.5      # 0=calm, 1=activated
    valence: float = 0.0      # -1=negative, +1=positive
    coherence: float = 0.5    # 0=confused, 1=clear
    tension: float = 0.0      # 0=relaxed, 1=strained
    
    def stress_level(self) -> float:
        """Combined stress metric"""
        return (self.arousal * (1 - self.valence) / 2) * (1 - self.coherence)
    
    def needs_break(self) -> bool:
        """Should enter rest/dream state"""
        return self.stress_level() > 0.8 or self.tension > 0.9
    
    def adjust_thinking_params(self) -> dict:
        """Somatic state controls thinking parameters"""
        if self.stress_level() > 0.7:
            # Stressed: think faster, shallower
            return {
                "intuitive_burst_size": 3,
                "dialogue_rounds": 1,
                "temperature": 0.3
            }
        elif self.arousal < 0.3:
            # Bored: explore more
            return {
                "intuitive_burst_size": 15,
                "dialogue_rounds": 5,
                "temperature": 0.9
            }
        else:
            # Balanced
            return {
                "intuitive_burst_size": 7,
                "dialogue_rounds": 3,
                "temperature": 0.7
            }
```

### 3. PNG Body

```python
# src/png_body.py
import numpy as np
from PIL import Image
from enum import Enum

class PatternType(Enum):
    GLIDER = "flowing_thought"
    BLOCK = "stable_belief"
    BLINKER = "oscillating_idea"
    CHAOS = "confusion"
    EMPTY = "mental_rest"

class PNGBody:
    """Conway's Game of Life as cognitive body"""
    
    def __init__(self, size=64):
        self.size = size
        self.grid = np.zeros((size, size), dtype=np.uint8)
        self.generation = 0
        self.history = []
        
    def inject_thought_pattern(self, thought_type: str, intensity: float):
        """Different thoughts create different patterns"""
        x, y = self._hash_to_position(thought_type)
        
        if "intuitive" in thought_type:
            self._inject_glider(x, y, intensity)
        elif "analytical" in thought_type:
            self._inject_block(x, y, int(intensity * 4))
        elif "conflict" in thought_type:
            self._inject_chaos(x, y, intensity)
            
    def evolve(self, steps: int = 1):
        """Run Game of Life rules"""
        for _ in range(steps):
            self.grid = self._apply_rules(self.grid)
            self.generation += 1
            
    def measure_state(self) -> dict:
        """Extract cognitive health metrics"""
        total_cells = np.sum(self.grid)
        density = total_cells / (self.size * self.size)
        
        # Detect patterns
        patterns = self._detect_patterns()
        
        return {
            "density": density,
            "stability": self._calculate_stability(),
            "patterns": patterns,
            "health": self._cognitive_health(density, patterns)
        }
    
    def _cognitive_health(self, density: float, patterns: dict) -> str:
        """Interpret pattern as cognitive state"""
        if density > 0.7:
            return "overwhelmed"
        elif density < 0.1:
            return "understimulated"
        elif patterns["oscillators"] > 5:
            return "looping"
        elif patterns["gliders"] > 3:
            return "flowing"
        else:
            return "balanced"
    
    def to_png(self, scale: int = 8) -> Image:
        """Export current state as PNG"""
        # Scale up for visibility
        scaled = np.kron(self.grid, np.ones((scale, scale)))
        # Add colors based on patterns
        colored = self._colorize(scaled)
        return Image.fromarray(colored, mode='RGB')
```

### 4. Cognitive Workout Nodes

```python
# src/workout_nodes.py
from pocketflow import Node
import asyncio

class TimeUnderTensionNode(Node):
    """Maintains cognitive tension for strength building"""
    
    def exec(self, shared):
        tension_time = time.time() - shared["tension_start"]
        shared["somatic"].tension = min(1.0, tension_time / shared["max_tension"])
        
        # Longer tension = deeper insights
        if tension_time < 5:
            return "warming_up"
        elif tension_time < 15:
            return "building_strength"
        elif tension_time < 30:
            return "peak_performance"
        else:
            return "needs_rest"
    
    def post(self, shared, prep_res, exec_res):
        shared["workout_phase"] = exec_res
        # Inject appropriate pattern
        shared["png_state"].inject_thought_pattern(
            f"tension_{exec_res}", 
            shared["somatic"].tension
        )
        return "continue" if exec_res != "needs_rest" else "dream"

class ProgressiveOverloadNode(Node):
    """Gradually increase question complexity"""
    
    def __init__(self):
        self.completed_workouts = []
        self.current_difficulty = 1
        
    def exec(self, performance_metrics):
        if performance_metrics["coherence"] > 0.8:
            # Success - increase difficulty
            self.current_difficulty = min(10, self.current_difficulty + 1)
            return "level_up"
        elif performance_metrics["stress"] > 0.8:
            # Too hard - decrease difficulty
            self.current_difficulty = max(1, self.current_difficulty - 1)
            return "scale_back"
        else:
            return "maintain"
```

### 5. MCP Server Interface

```python
# src/mcp_server.py
from typing import AsyncIterator
import json

class MindGymMCPServer:
    """MCP server exposing Mind Gym as a tool"""
    
    def __init__(self):
        self.gym = BicameralFlow()
        self.workout_history = []
        
    async def start_workout(self, query: str, workout_type: str = "standard") -> AsyncIterator[str]:
        """Stream thoughts during workout"""
        
        # Select workout parameters
        if workout_type == "quick":
            max_tension = 10.0
            target_rounds = 2
        elif workout_type == "deep":
            max_tension = 60.0
            target_rounds = 10
        else:
            max_tension = 30.0
            target_rounds = 5
            
        # Stream thoughts
        thought_count = 0
        async for thought in self.gym.think(query, max_tension):
            thought_count += 1
            
            # Format for MCP
            response = {
                "thought_number": thought_count,
                "speaker": thought["speaker"],
                "content": thought["content"],
                "somatic_state": thought["somatic"].dict(),
                "workout_phase": thought.get("workout_phase", "active"),
                "png_snapshot": self._encode_png_preview(thought["png_state"])
            }
            
            yield json.dumps(response)
            
            # Check if workout complete
            if thought.get("synthesis") or thought_count > target_rounds:
                break
    
    async def get_workout_summary(self, workout_id: str) -> dict:
        """Analyze completed workout"""
        workout = self.workout_history[workout_id]
        
        return {
            "duration": workout["end_time"] - workout["start_time"],
            "thoughts_generated": len(workout["thoughts"]),
            "cognitive_load_curve": workout["load_curve"],
            "breakthrough_moments": workout["breakthroughs"],
            "recommendation": self._generate_recommendation(workout)
        }
```

### 6. Local Development Tools

```python
# src/cli.py
import click
import asyncio

@click.command()
@click.option('--query', prompt='What would you like to think about?')
@click.option('--workout', default='standard', type=click.Choice(['quick', 'standard', 'deep']))
@click.option('--visualize/--no-visualize', default=True)
async def workout(query, workout, visualize):
    """Run a mind gym workout session"""
    gym = MindGymMCPServer()
    
    print(f"\n🧠 Starting {workout} workout: '{query}'\n")
    
    async for thought_json in gym.start_workout(query, workout):
        thought = json.loads(thought_json)
        
        # Display thought
        print(f"[{thought['speaker']}] {thought['content']}")
        
        # Show somatic state
        somatic = thought['somatic_state']
        print(f"   Arousal: {'▓' * int(somatic['arousal'] * 10)}")
        print(f"   Tension: {'▓' * int(somatic['tension'] * 10)}")
        
        # Optionally show PNG
        if visualize and thought['thought_number'] % 5 == 0:
            png = decode_png_preview(thought['png_snapshot'])
            png.show()
            
    print("\n✅ Workout complete!")

if __name__ == '__main__':
    asyncio.run(workout())
```

## Testing Strategy

### Unit Tests
- Somatic state transitions
- PNG pattern evolution
- Node execution logic

### Integration Tests
- Full workout flows
- Dream state branching
- MCP protocol compliance

### User Tests
Test with these query types:
1. **Simple**: "What is happiness?"
2. **Complex**: "How does consciousness emerge?"
3. **Creative**: "Design a new musical instrument"
4. **Personal**: "How should I approach difficult conversations?"

## Success Metrics

1. **Cognitive Coherence**: Synthesis incorporates both hemispheres
2. **Workout Completion**: 80% of sessions reach synthesis
3. **Pattern Health**: PNG shows balanced patterns (not stuck/chaotic)
4. **User Engagement**: Average session > 5 minutes
5. **Novel Insights**: Users report new perspectives

## Development Timeline

### Week 1: Core Infrastructure
- [ ] PocketFlow integration
- [ ] Basic bicameral flow
- [ ] Somatic state tracking
- [ ] Simple PNG generation

### Week 2: Cognitive Features
- [ ] Map/reduce implementation
- [ ] Time under tension
- [ ] Progressive overload
- [ ] Dream state basics

### Week 3: Polish & Deploy
- [ ] MCP server
- [ ] CLI interface
- [ ] Docker container
- [ ] Documentation

## Future Enhancements

1. **Multi-agent hive** - Multiple bicameral agents collaborating
2. **Long-term memory** - Persistent workout history
3. **Custom workouts** - User-defined thinking exercises
4. **Pattern library** - Catalog of healthy/unhealthy patterns
5. **Fine-tuning** - Optimize local model for intuitive role

## Quick Start

```bash
# Clone repo
git clone https://github.com/yourusername/mind-gym
cd mind-gym

# Install dependencies
pip install -e .

# Download local model
python scripts/download_model.py --model mistral-7b-instruct

# Set API keys
export ANTHROPIC_API_KEY=your_key_here

# Run a workout
python -m mindgym.cli --query "What is consciousness?" --workout deep

# Start MCP server
python -m mindgym.server --port 3000
```

## Dependencies

```toml
[project]
name = "mind-gym"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "pocketflow>=0.1.0",
    "anthropic>=0.18.0",
    "llama-cpp-python>=0.2.0",
    "pillow>=10.0.0",
    "numpy>=1.24.0",
    "click>=8.1.0",
    "gitpython>=3.1.0",
    "asyncio>=3.11.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
]
```

This MVP delivers a working Mind Gym that demonstrates all core concepts while remaining buildable in 3 weeks!