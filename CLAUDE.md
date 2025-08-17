# CLAUDE.md - Mind Gym Project Context

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🎯 Current Development Status

### Active Sprint: Week 1 - PocketFlow Integration
- **Branch**: main (PR #2 pending merge for GitHub infrastructure)
- **Epic in Progress**: #9 - PocketFlow Integration
- **Issues Created**: #1-#23 (infrastructure + epics + Week 1 tasks)
- **Next Milestone**: Complete PocketFlow foundation by end of Week 1

### Completed Work
✅ GitHub infrastructure (Issue #1, PR #2)
✅ All 7 Epic issues created (#9-#15)
✅ Week 1 implementation issues created (#16-#23)
✅ Project documentation (README, CONTRIBUTING, ARCHITECTURE)

### GitHub Issues Overview
- **Epics Created**: 
  - #9: PocketFlow Integration (Week 1)
  - #10: Bicameral Engine (Week 2)
  - #11: Somatic Feedback System (Week 2)
  - #12: PNG Body Visualization (Week 2-3)
  - #13: Cognitive Workout System (Week 2-3)
  - #14: Dream States & Git Integration (Week 3)
  - #15: MCP Server & Interface (Week 3)

- **Week 1 Tasks** (Ready for development):
  - #16: Setup Python Package Structure (S)
  - #17: Install and Configure PocketFlow (S)
  - #18: Implement Base Node Class (M)
  - #19: Implement Flow Class (M)
  - #20: Create Shared State System (M)
  - #21: Add Async Generator Support (M)
  - #22: Create Basic Unit Tests (L)
  - #23: Setup Development Environment (S)

## 🧠 Project Overview

You are helping build the **Mind Gym** - a bicameral AI agent system that "exercises" its thinking abilities like a weightlifter builds muscle. The system has two "minds" (intuitive/analytical) that engage in internal dialogue, regulated by a somatic feedback layer and visualized through an evolving Conway's Game of Life pattern.

## 🏗️ Architecture Summary

### Core Components
1. **PocketFlow**: 100-line LLM orchestration framework (Week 1)
2. **Bicameral Engine**: Dual mind system with internal dialogue (Week 2)
3. **Somatic Layer**: Emotional state modulation (Week 2)
4. **PNG Body**: Conway's Game of Life visualization (Week 2-3)
5. **Workout System**: Cognitive exercise framework (Week 2-3)
6. **Dream States**: Git-based exploration (Week 3)
7. **MCP Server**: External interface (Week 3)

### Key Design Patterns

#### PocketFlow Node Pattern
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

#### Async Generator Pattern
```python
async def thinking_process(query: str) -> AsyncIterator[Thought]:
    # Stream thoughts as they emerge
    async for thought in generate_thoughts(query):
        yield thought
```

#### Somatic Feedback Pattern
```python
if somatic.stress_level() > 0.7:
    # Reduce complexity when stressed
    params["temperature"] = 0.3
    params["burst_size"] = 3
```

## 📁 Repository Structure

```
tool-mind-gym/
├── .github/              # GitHub templates and workflows
│   ├── ISSUE_TEMPLATE/   # Issue templates
│   ├── workflows/        # CI/CD workflows
│   └── pull_request_template.md
├── src/mind_gym/         # Main package (to be implemented)
│   ├── __init__.py
│   ├── engine.py         # Bicameral engine
│   ├── nodes/            # PocketFlow nodes
│   ├── somatic.py        # Emotional layer
│   ├── png_body.py       # Visual patterns
│   ├── server.py         # MCP server
│   └── cli.py            # Command line
├── tests/                # Test suites
│   ├── unit/
│   ├── integration/
│   └── cognitive/
├── docs/                 # Design documents
├── scripts/              # Utility scripts
├── ARCHITECTURE.md       # System design
├── CONTRIBUTING.md       # Team guidelines
├── README.md            # Setup instructions
└── pyproject.toml       # Python configuration
```

## 🚀 Development Workflow

### Current Phase
1. **Complete PR #2 merge** - Get GitHub infrastructure into main
2. **Start Issue #16** - Setup Python package structure
3. **Follow dependency chain** - Work through Week 1 issues in order

### Issue Workflow
1. Pick issue from GitHub Project Board
2. Create feature branch: `feature/issue-{number}-description`
3. Implement with tests
4. Create PR linking to issue
5. Get review and merge

### Testing Requirements
- Unit tests for all new code
- Integration tests for component interactions
- Cognitive tests for AI behavior
- Minimum 80% code coverage

## 🎓 Key Concepts to Remember

### Bicameral Architecture
- **Intuitive Mind**: Fast, creative, runs on local LLM (7-13B)
- **Analytical Mind**: Slow, logical, runs on API LLM (Claude/GPT-4)
- Internal dialogue produces synthesis

### Cognitive Exercise Principles
- **Time Under Tension**: Holding cognitive tension builds insight
- **Progressive Overload**: Gradually increasing complexity
- **Rest/Recovery**: Dream states for consolidation

### Unique Features
- **Git-based Dreams**: Exploration on branches
- **Somatic Control**: Emotional state modulates thinking
- **PNG as Function**: Visual patterns affect cognition
- **Map/Reduce Sync**: Handles different thinking speeds

## 📝 Implementation Priorities

### Week 1 (Current)
Focus on PocketFlow foundation:
- Python package structure
- Node and Flow classes
- Shared state system
- Async streaming support
- Basic unit tests

### Week 2 (Next)
Build core thinking system:
- LLM wrappers (API + local)
- Bicameral nodes
- Internal dialogue
- Somatic feedback
- PNG visualization start

### Week 3 (Future)
Advanced features:
- Workout system
- Dream states
- MCP server
- Integration testing

## ⚠️ Important Context

- **Performance**: Intentionally slow (minutes not milliseconds)
- **Not a Chatbot**: This is genuine cognitive exercise
- **Observable Thinking**: Make internal processes visible
- **Pythonic Design**: Use Python idioms over abstractions
- **Test Complexity**: Simple → Complex → Creative → Personal

## 📊 Testing Strategy

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
- Genuine insights

## 🔗 Key References

### Design Documents
- `mind-gym-mvp-prd.md` - Complete MVP specification
- `bicameral-mcp-mvp-prd.md` - MCP server details
- `ARCHITECTURE.md` - System architecture
- `CONTRIBUTING.md` - Development guidelines

### Implementation Status
- `WEEK1_IMPLEMENTATION_STATUS.md` - Current sprint status
- GitHub Issues #16-23 - Week 1 tasks with details
- GitHub Project Board - Visual workflow

## 💡 Development Philosophy

- Start simple, add complexity only when needed
- Make the thinking process observable
- Embrace Python's strengths (async, generators, decorators)
- Focus on genuine cognitive development, not just Q&A
- The AI should know when it's confused or tired

## 🎯 Success Metrics

- Bicameral dialogue produces genuine insights
- Somatic layer prevents unhealthy patterns
- PNG patterns show thought formation
- System knows when to rest vs push
- Dreams produce novel connections

---

**Remember**: We're not building a faster chatbot. We're building an AI that genuinely contemplates, struggles, learns, and grows stronger through the process of thinking itself.

**Last Updated**: 2025-08-17
**Current Issue Focus**: #16 - Setup Python Package Structure
**Next Major Milestone**: Complete PocketFlow Integration (End of Week 1)