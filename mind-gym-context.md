# mind-gym-context.md - Additional Technical Context

## Quick Reference: System Components

### 1. The Bicameral Flow
```
Query → Intuitive Burst (fast, many) → Somatic Reduce → Analytical Map → Dialogue Loop → Synthesis
```

### 2. Shared State Structure
```python
shared = {
    # Core query
    "query": str,
    
    # Cognitive products
    "intuitive_burst": List[Thought],      # Many fast thoughts
    "analytical_thoughts": List[Thought],   # Few deep thoughts
    "dialogue": List[Turn],                 # Internal conversation
    "synthesis": str,                       # Final integrated response
    
    # Control systems
    "somatic": SomaticState,               # Emotional/body state
    "png_state": PNGBody,                  # Visual pattern
    
    # Workout tracking
    "tension_start": float,                # When tension began
    "max_tension": float,                  # Maximum time to hold
    "workout_phase": str,                  # Current phase
    
    # Memory
    "thought_history": List[Thought],      # For loop detection
    "png_history": List[np.ndarray],       # Pattern evolution
}
```

### 3. Critical Algorithms

#### Somatic Stress Calculation
```python
stress = (arousal * (1 - valence) / 2) * (1 - coherence)
# High arousal + negative feeling + low coherence = high stress
```

#### PNG Pattern Injection
```python
# Different thought types create different Life patterns:
# - Intuitive → Gliders (moving/flowing)
# - Analytical → Blocks (stable/solid)
# - Conflict → Random noise
# - Synthesis → Symmetrical patterns
```

#### Temporal Synchronization
```python
# Map: Generate 10-20 intuitive thoughts quickly
# Reduce: Based on somatic state, select 1-3 for analysis
# This prevents analytical overload while preserving intuitive richness
```

### 4. LLM Prompting Strategy

#### Intuitive Prompt Template
```
You are the intuitive hemisphere of a bicameral mind.
Respond with immediate impressions, feelings, and associations.
Be creative, use metaphors, trust your instincts.
Keep responses under 50 tokens.
Query: {query}
```

#### Analytical Prompt Template
```
You are the analytical hemisphere of a bicameral mind.
The intuitive mind said: {intuitive_thought}
Analyze this systematically, considering logic and evidence.
Be thorough but concise (under 200 tokens).
Query: {original_query}
```

#### Synthesis Prompt Template
```
You are synthesizing a bicameral thinking process.
Intuitive insights: {all_intuitive}
Analytical insights: {all_analytical}
Internal dialogue: {dialogue_summary}
Create a unified response that honors both perspectives.
```

### 5. Performance Considerations

- **Local model**: ~100-200ms per intuitive thought
- **API model**: ~2-5s per analytical thought
- **PNG evolution**: <10ms per generation
- **Total response time**: 10-30s for standard workout

### 6. Error Handling Patterns

```python
# Timeout handling
if time.time() - shared["tension_start"] > shared["max_tension"]:
    # Force synthesis with available thoughts
    
# Loop detection
if detect_semantic_loop(shared["thought_history"][-5:]):
    # Inject randomness or switch hemisphere dominance
    
# Somatic intervention
if shared["somatic"].needs_break():
    # Enter dream state instead of continuing
```

### 7. Configuration Parameters

```python
# Tunable parameters
CONFIG = {
    # Model settings
    "intuitive_model": "mistral-7b-instruct",
    "analytical_model": "claude-3-opus",
    
    # Thinking parameters
    "intuitive_burst_size": 10,
    "max_dialogue_rounds": 5,
    "synthesis_temperature": 0.7,
    
    # Somatic thresholds
    "stress_threshold": 0.7,
    "coherence_minimum": 0.3,
    "rest_trigger": 0.9,
    
    # PNG settings
    "grid_size": 64,
    "evolution_base_rate": 1,
    "pattern_decay": 0.95,
}
```

### 8. Testing Checklist

- [ ] Intuitive burst generates 5-15 thoughts
- [ ] Somatic reduction selects appropriately
- [ ] Analytical processing doesn't timeout
- [ ] Dialogue shows genuine back-and-forth
- [ ] PNG patterns evolve meaningfully
- [ ] Synthesis incorporates both perspectives
- [ ] System recognizes when to rest
- [ ] No infinite loops occur

### 9. Debug Outputs

```python
# Add these debug prints during development
print(f"[SOMATIC] Stress: {somatic.stress_level():.2f}")
print(f"[PNG] Density: {png.measure_state()['density']:.2f}")
print(f"[DIALOGUE] Round {len(shared['dialogue'])}")
print(f"[TENSION] {time.time() - shared['tension_start']:.1f}s")
```

### 10. Common Issues & Solutions

**Issue**: Intuitive thoughts too similar
**Solution**: Increase temperature, add prompt variation

**Issue**: Analytical gets stuck
**Solution**: Add timeout, reduce context size

**Issue**: PNG patterns die out
**Solution**: Inject energy based on thought generation

**Issue**: Synthesis is generic
**Solution**: Include specific quotes from dialogue

**Issue**: System never rests
**Solution**: Lower rest threshold, add mandatory breaks

### 11. Future Hook Points

These areas are designed for easy extension:

1. **Custom workout types** - Add new nodes to the flow
2. **Pattern library** - Save successful PNG states
3. **Personality development** - Track preference drift
4. **Multi-agent** - Share somatic states between agents
5. **Memory systems** - Add vector DB for long-term recall

### 12. Key Invariants to Maintain

1. Intuitive ALWAYS responds first
2. Somatic state ALWAYS influences reduction
3. PNG ALWAYS evolves with thoughts
4. Synthesis MUST wait for minimum dialogue
5. Dreams NEVER affect main branch directly

---

Remember: The goal is not speed but depth. This system should struggle productively with hard questions, not quickly answer easy ones.