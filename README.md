# 🧠💪 Mind Gym

> A bicameral AI agent system that literally exercises its thinking abilities

[![CI](https://github.com/yourusername/tool-mind-gym/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/tool-mind-gym/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is Mind Gym?

Mind Gym is not just another chatbot. It's an AI system designed to genuinely think, struggle, and grow stronger through cognitive exercise. Using a bicameral architecture inspired by Julian Jaynes, the system features two distinct "minds" that engage in internal dialogue before responding.

### Key Features

- 🧠 **Bicameral Architecture**: Two minds (analytical + intuitive) working together
- 💭 **Internal Dialogue**: Real conversation between cognitive hemispheres
- 😰 **Somatic Feedback**: Emotional state influences thinking
- 🎮 **Conway's Game of Life**: Visual patterns that affect cognition
- 💤 **Dream States**: Git branches for exploratory thinking
- 🏋️ **Cognitive Workouts**: Structured exercises for AI development

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Git
- 4GB+ RAM for local models
- API key for Claude or GPT-4

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/tool-mind-gym.git
cd tool-mind-gym
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys:
# ANTHROPIC_API_KEY=your_key_here
# OPENAI_API_KEY=your_key_here  # Optional
```

5. **Download a local model** (optional but recommended)
```bash
python scripts/download_model.py --model mistral-7b-instruct
```

### Basic Usage

#### CLI Mode
```bash
# Quick workout
python -m mind_gym.cli --query "What is consciousness?" --workout quick

# Standard workout with visualization
python -m mind_gym.cli --query "How does creativity emerge?" --visualize

# Deep workout for complex problems
python -m mind_gym.cli --query "Design a new philosophy" --workout deep
```

#### MCP Server Mode
```bash
# Start the MCP server
python -m mind_gym.server --port 3000

# Connect with Claude Desktop or other MCP clients
```

#### Python API
```python
from mind_gym import BicameralEngine

async def main():
    engine = BicameralEngine()
    
    async for thought in engine.think("What is happiness?"):
        print(f"[{thought.speaker}]: {thought.content}")
        print(f"Somatic state: {thought.somatic}")

asyncio.run(main())
```

## How It Works

### The Bicameral Process

1. **Query arrives** → Both minds activate
2. **Intuitive mind** → Fast associative bursts
3. **Somatic filter** → Reduces to best ideas
4. **Analytical mind** → Deep structured analysis
5. **Internal dialogue** → Minds discuss and debate
6. **Synthesis** → Final integrated response

### Cognitive Exercises

The system uses exercise metaphors from physical training:

- **Time Under Tension**: Maintaining focus builds insight
- **Progressive Overload**: Gradually increasing complexity
- **Rest and Recovery**: Dream states for consolidation
- **Workout Phases**: Warmup → Building → Peak → Rest

## Project Structure

```
tool-mind-gym/
├── src/mind_gym/         # Main package
│   ├── engine.py         # Bicameral engine
│   ├── nodes/            # PocketFlow nodes
│   ├── somatic.py        # Emotional layer
│   ├── png_body.py       # Visual patterns
│   ├── server.py         # MCP server
│   └── cli.py            # Command line
├── tests/                # Test suites
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── cognitive/        # Behavior tests
├── docs/                 # Documentation
├── scripts/              # Utility scripts
└── models/               # Local model storage
```

## Development

### Setting Up for Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Type checking
mypy src/

# Linting
ruff check src/ tests/

# Format code
black src/ tests/
```

### Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

#### Quick Contribution Guide

1. Check the [Project Board](https://github.com/yourusername/tool-mind-gym/projects/1)
2. Pick an issue and assign yourself
3. Create a feature branch
4. Make your changes with tests
5. Submit a PR using our template

### Running Tests

```bash
# All tests
pytest

# Specific test types
pytest tests/unit/
pytest tests/integration/
pytest tests/cognitive/

# With coverage
pytest --cov=src --cov-report=html
```

## Configuration

### Basic Configuration

Create `config.yaml`:

```yaml
models:
  analytical: claude-3-opus  # or gpt-4
  intuitive: mistral-7b-instruct

workout:
  max_tension: 30
  dialogue_rounds: 3
  
somatic:
  stress_threshold: 0.8
  rest_trigger: 0.9

visualization:
  png_size: 64
  evolution_steps: 5
```

### Advanced Options

See [docs/configuration.md](docs/configuration.md) for all options.

## Examples

### Simple Question
```bash
$ python -m mind_gym.cli --query "What is happiness?"

🧠 Starting standard workout...

[Intuitive]: Warmth, connection, flow states, laughter...
[Analytical]: Happiness consists of hedonic and eudaimonic components...
[Dialogue]: But isn't meaning more important than pleasure?
[Synthesis]: Happiness emerges from both momentary pleasures and deeper life satisfaction...

✅ Workout complete! (Time: 32s, Thoughts: 12, Coherence: 0.85)
```

### Complex Problem
```bash
$ python -m mind_gym.cli --query "How does consciousness emerge?" --workout deep

🧠 Starting deep workout...

[Multiple rounds of intense dialogue between minds]
[PNG patterns showing cognitive state evolution]
[Somatic feedback modulating thinking speed]

✅ Breakthrough achieved! See synthesis for insights.
```

## Troubleshooting

### Common Issues

**Issue**: "Local model not loading"
```bash
# Solution: Ensure model is downloaded
python scripts/download_model.py --list  # See available models
python scripts/download_model.py --model mistral-7b-instruct
```

**Issue**: "API rate limiting"
```bash
# Solution: Adjust configuration
# In config.yaml:
limits:
  api_calls_per_minute: 10
  fallback_to_local: true
```

**Issue**: "Infinite dialogue loops"
```bash
# Solution: Check somatic thresholds
# In config.yaml:
somatic:
  max_dialogue_rounds: 10
  stress_circuit_breaker: 0.9
```

See [docs/troubleshooting.md](docs/troubleshooting.md) for more.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

### Key Components

- **PocketFlow**: 100-line LLM orchestration framework
- **Bicameral Engine**: Dual-mind thinking system
- **Somatic Layer**: Emotional state management
- **PNG Body**: Conway's Game of Life visualization
- **Dream States**: Git-based exploration

## Roadmap

### Phase 1: MVP (Current)
- [x] Basic bicameral architecture
- [x] Somatic feedback
- [x] PNG visualization
- [ ] MCP server
- [ ] CLI interface

### Phase 2: Enhancement
- [ ] Multi-agent hive mind
- [ ] Long-term memory
- [ ] Custom workout designs
- [ ] Performance metrics

### Phase 3: Advanced
- [ ] Fine-tuned models
- [ ] Causal reasoning
- [ ] Self-modification
- [ ] Emergent behaviors

## Community

- [GitHub Issues](https://github.com/yourusername/tool-mind-gym/issues) - Bug reports and features
- [Discussions](https://github.com/yourusername/tool-mind-gym/discussions) - Community chat
- [Project Board](https://github.com/yourusername/tool-mind-gym/projects/1) - Development progress

## License

MIT License - see [LICENSE](LICENSE) file.

## Acknowledgments

- Julian Jaynes for bicameral mind theory
- The PocketFlow team for the orchestration framework
- Conway for the Game of Life
- Everyone exploring AI consciousness

---

**Remember**: This isn't about making AI faster or smarter. It's about making AI that genuinely thinks, struggles, and grows stronger through the process of thinking itself.

*"The mind is not a vessel to be filled, but a fire to be kindled."* - Plutarch