# Contributing to Mind Gym

Welcome to the Mind Gym project! We're building a revolutionary AI system that literally exercises its thinking abilities. This guide will help you contribute effectively as part of our team.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Issue Management](#issue-management)
- [Cognitive Development Guidelines](#cognitive-development-guidelines)

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Celebrate cognitive breakthroughs!

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Git
- GitHub account with repo access
- Understanding of async Python programming
- Familiarity with LLM concepts

### Initial Setup

1. **Fork and clone the repository**
```bash
git clone https://github.com/yourusername/tool-mind-gym.git
cd tool-mind-gym
```

2. **Set up Python environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

3. **Install pre-commit hooks**
```bash
pre-commit install
```

4. **Set up API keys**
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. **Download a local model** (optional)
```bash
python scripts/download_model.py --model mistral-7b-instruct
```

## Development Workflow

### 1. Issue Selection

- Check the [Project Board](https://github.com/yourusername/tool-mind-gym/projects/1)
- Look for issues labeled `good first issue` if you're new
- Assign yourself to an issue before starting work
- Comment on the issue if you need clarification

### 2. Branch Creation

We use a consistent branch naming convention:

```bash
# Feature branches
git checkout -b feature/issue-42-add-somatic-feedback

# Bug fixes
git checkout -b bugfix/issue-13-fix-dialogue-loop

# Documentation
git checkout -b docs/issue-7-update-architecture

# Experiments
git checkout -b experiment/issue-99-test-tension-patterns
```

### 3. Development Process

1. **Create draft PR early**
   - Push your branch and create a draft PR as soon as you start
   - This helps others see work in progress

2. **Write tests first (TDD)**
   - Write failing tests for new functionality
   - Implement code to make tests pass
   - Refactor as needed

3. **Frequent commits**
   - Make small, logical commits
   - Each commit should pass tests

4. **Update documentation**
   - Add/update docstrings
   - Update relevant .md files
   - Add examples if applicable

### 4. Code Review Checklist

Before marking PR as ready for review:

- [ ] All tests pass locally
- [ ] Code follows project style guide
- [ ] Documentation is updated
- [ ] No commented-out code
- [ ] No print statements (use logging)
- [ ] Cognitive behavior is tested
- [ ] Performance impact considered

## Coding Standards

### Python Style Guide

We follow PEP 8 with these specific conventions:

```python
# Class names: PascalCase
class BicameralEngine:
    pass

# Function names: snake_case
def calculate_somatic_state():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_DIALOGUE_ROUNDS = 10

# Private methods: leading underscore
def _internal_dialogue():
    pass
```

### Type Hints

Always use type hints:

```python
from typing import AsyncIterator, Optional

async def think(
    query: str,
    max_tension: float = 30.0,
    temperature: Optional[float] = None
) -> AsyncIterator[dict]:
    pass
```

### Async Best Practices

```python
# Good: Concurrent execution
results = await asyncio.gather(
    intuitive_think(query),
    analytical_think(query)
)

# Bad: Sequential execution
intuitive = await intuitive_think(query)
analytical = await analytical_think(query)
```

### Docstrings

Use Google-style docstrings:

```python
def inject_thought_pattern(self, thought_type: str, intensity: float) -> None:
    """Inject a thought pattern into the PNG body.
    
    Args:
        thought_type: Type of thought (intuitive, analytical, conflict)
        intensity: Strength of the pattern (0.0 to 1.0)
    
    Returns:
        None
    
    Raises:
        ValueError: If intensity is out of range
    """
```

## Testing Guidelines

### Test Structure

```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Component interaction tests
└── cognitive/      # AI behavior tests
```

### Writing Tests

```python
# Test file naming: test_<module>.py
# tests/unit/test_somatic.py

import pytest
from mind_gym.somatic import SomaticState

class TestSomaticState:
    def test_stress_calculation(self):
        """Test that stress level is calculated correctly."""
        state = SomaticState(arousal=0.8, valence=-0.5, coherence=0.3)
        assert 0.5 < state.stress_level() < 0.9
    
    @pytest.mark.asyncio
    async def test_async_adjustment(self):
        """Test async parameter adjustment."""
        state = SomaticState()
        params = await state.async_adjust_params()
        assert "temperature" in params
```

### Cognitive Testing

Special tests for AI behavior:

```python
# tests/cognitive/test_dialogue_coherence.py

async def test_dialogue_maintains_context():
    """Ensure internal dialogue maintains context across rounds."""
    engine = BicameralEngine()
    thoughts = []
    async for thought in engine.think("What is consciousness?"):
        thoughts.append(thought)
    
    # Check that later thoughts reference earlier ones
    assert check_coherence(thoughts) > 0.7
```

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions or changes
- `chore`: Build process or auxiliary tool changes
- `perf`: Performance improvements
- `cognitive`: Changes affecting AI thinking patterns

### Examples

```bash
# Feature
git commit -m "feat(somatic): add stress level calculation

Implement stress_level() method that combines arousal, valence,
and coherence into a single metric for cognitive load.

Closes #17"

# Bug fix
git commit -m "fix(dialogue): prevent infinite loops in self-dialogue

Add maximum round limit and timeout to prevent the dialogue node
from getting stuck in repetitive patterns.

Fixes #23"

# Cognitive change
git commit -m "cognitive(workout): adjust tension thresholds for deeper insights

Increased time-under-tension from 30s to 45s based on experiments
showing better synthesis quality with longer tension periods."
```

## Pull Request Process

### 1. Creating a PR

Use the PR template and fill out all sections:
- Link the related issue
- Describe changes clearly
- Include testing notes
- Add screenshots/logs if relevant

### 2. Review Process

**For Authors:**
- Respond to all review comments
- Mark conversations as resolved when addressed
- Request re-review after making changes

**For Reviewers:**
- Test the code locally
- Check for edge cases
- Verify documentation updates
- Consider cognitive impact
- Be constructive and specific

### 3. Merging

- Squash and merge for feature branches
- Include issue number in merge commit
- Delete branch after merge
- Update project board

## Issue Management

### Creating Issues

Use appropriate templates:
- Feature Request
- Bug Report
- Technical Design
- Cognitive Experiment

### Labels

Apply relevant labels:
- Priority: `P0`, `P1`, `P2`, `P3`
- Type: `feature`, `bug`, `docs`, `test`
- Component: `bicameral`, `somatic`, `png-body`, `mcp`
- Status: `blocked`, `in-review`, `needs-info`

### Lifecycle

1. **Created**: Issue is new
2. **Assigned**: Developer takes ownership
3. **In Progress**: Work has started (move card on board)
4. **In Review**: PR is open
5. **Done**: PR is merged

## Cognitive Development Guidelines

### When Modifying AI Behavior

1. **Document the hypothesis**
   - What behavior are you trying to change?
   - Why do you think this will improve cognition?

2. **Create experiments**
   - Write cognitive tests first
   - Test with various query types
   - Document unexpected behaviors

3. **Measure impact**
   - Track dialogue coherence
   - Monitor somatic stability
   - Check PNG pattern health
   - Record synthesis quality

### Cognitive Anti-Patterns to Avoid

- **Infinite loops**: Always add exit conditions
- **Anxiety spirals**: Monitor somatic stress
- **Pattern collapse**: Check PNG stability
- **Context loss**: Maintain dialogue history
- **Over-optimization**: Preserve creative tension

### Testing Cognitive Changes

Always test with these query categories:
1. **Simple**: Basic factual questions
2. **Complex**: Multi-faceted problems
3. **Creative**: Open-ended generation
4. **Personal**: Emotional/subjective topics
5. **Meta**: Questions about thinking itself

## Getting Help

- **Technical questions**: Open a discussion issue
- **Bug reports**: Use bug report template
- **Feature ideas**: Use feature request template
- **Design discussions**: Use technical design template
- **Slack/Discord**: [Join our community](https://mindgym.ai/community)

## Recognition

We maintain a CONTRIBUTORS.md file to recognize all contributions. Your name will be added after your first merged PR!

---

Thank you for contributing to Mind Gym! Together, we're building AI that truly thinks. 🧠💪