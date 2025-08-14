# SICP-Aligned Agent State Management System
## Revised Project Proposal

### Executive Summary

A procedural approach to agent state management that emphasizes simplicity, composability, and clear abstractions. The system builds complex agent behaviors from simple primitives using function composition, explicit state management, and data-driven behavior trees. No monads required.

### Core Philosophy (The SICP Way)

1. **Start simple** - Basic functions that transform state
2. **Compose naturally** - Build complex behaviors from simple ones
3. **Data as interface** - Actions and behaviors are just data
4. **Clear evaluation** - You can trace execution with a pencil

### Technical Architecture

```
Agent System
├── Actions (simple data structures)
├── Behaviors (state -> action functions)
├── Composers (combine behaviors)
├── Interpreters (execute actions)
└── Graphs (behavior organization)
```

## Core Design

### 1. Actions as Data

```python
# Actions are just dictionaries with a type and data
def make_action(action_type, **data):
    return {'type': action_type, 'data': data}

# Examples
move_north = make_action('move', direction='north', distance=1)
attack_enemy = make_action('attack', target='nearest_enemy', damage=10)
wait = make_action('wait', duration=1)
```

### 2. State as Simple Data

```python
# State is explicit and simple
class AgentState:
    def __init__(self, position, health, inventory, world_view):
        self.position = position
        self.health = health
        self.inventory = inventory
        self.world_view = world_view  # What the agent can see
        self.history = []  # For time-travel debugging
    
    def copy(self):
        """Pure functions need state copies"""
        new_state = AgentState(
            position=self.position.copy(),
            health=self.health,
            inventory=self.inventory.copy(),
            world_view=self.world_view.copy()
        )
        new_state.history = self.history.copy()
        return new_state
```

### 3. Behaviors as Pure Functions

```python
# Behaviors are functions: State -> Action
def flee_behavior(state):
    """Run away from nearest threat"""
    threat = find_nearest_threat(state.world_view)
    if threat:
        direction = opposite_direction(state.position, threat.position)
        return make_action('move', direction=direction, distance=2)
    return make_action('wait')

def attack_behavior(state):
    """Attack nearest enemy if in range"""
    enemy = find_nearest_enemy(state.world_view)
    if enemy and distance(state.position, enemy.position) < 2:
        return make_action('attack', target=enemy.id, damage=10)
    return None  # No action

def explore_behavior(state):
    """Move to unexplored areas"""
    unexplored = find_unexplored_direction(state.world_view)
    return make_action('move', direction=unexplored, distance=1)
```

### 4. Behavior Composition

```python
# Simple composition patterns
def priority_behavior(*behaviors):
    """Try behaviors in order until one returns an action"""
    def composed(state):
        for behavior in behaviors:
            action = behavior(state)
            if action:
                return action
        return make_action('wait')
    return composed

def conditional_behavior(condition, then_behavior, else_behavior):
    """Choose behavior based on condition"""
    def composed(state):
        if condition(state):
            return then_behavior(state)
        else:
            return else_behavior(state)
    return composed

def weighted_behavior(behavior_weights):
    """Randomly choose behavior based on weights"""
    def composed(state):
        behavior = weighted_random_choice(behavior_weights)
        return behavior(state)
    return composed

# Example: Complex behavior from simple parts
cautious_agent = priority_behavior(
    flee_behavior,
    conditional_behavior(
        lambda s: s.health > 50,
        attack_behavior,
        explore_behavior
    )
)
```

### 5. Action Interpretation

```python
def interpret_action(action, state):
    """Execute action on state, returning new state"""
    new_state = state.copy()
    
    # Record history for debugging
    new_state.history.append((action, state))
    
    # Dispatch based on action type
    if action['type'] == 'move':
        new_state.position = update_position(
            state.position, 
            action['data']['direction'],
            action['data']['distance']
        )
    elif action['type'] == 'attack':
        # Apply damage, trigger events, etc.
        handle_attack(new_state, action['data'])
    elif action['type'] == 'wait':
        # Just advance time
        pass
    
    # Update world view after action
    new_state.world_view = compute_world_view(new_state)
    
    return new_state
```

### 6. Behavior Graphs (Node System)

```python
class BehaviorNode:
    def __init__(self, name, behavior, edges=None):
        self.name = name
        self.behavior = behavior
        self.edges = edges or {}  # condition -> next_node
    
    def evaluate(self, state):
        """Get action and next node"""
        action = self.behavior(state)
        
        # Determine next node based on conditions
        for condition, next_node in self.edges.items():
            if condition(state, action):
                return action, next_node
        
        return action, self  # Stay at current node

class BehaviorGraph:
    def __init__(self, nodes, start_node):
        self.nodes = {node.name: node for node in nodes}
        self.start_node = start_node
        self.current_node = start_node
    
    def get_action(self, state):
        """Get next action from current node"""
        node = self.nodes[self.current_node]
        action, next_node = node.evaluate(state)
        self.current_node = next_node
        return action

# Example: Patrol behavior graph
patrol_graph = BehaviorGraph([
    BehaviorNode('patrol', patrol_behavior, {
        see_enemy: 'combat',
        low_health: 'retreat'
    }),
    BehaviorNode('combat', attack_behavior, {
        enemy_dead: 'patrol',
        low_health: 'retreat'
    }),
    BehaviorNode('retreat', flee_behavior, {
        safe_distance: 'patrol'
    })
], start_node='patrol')
```

### 7. Advanced Features (Built Simply)

#### Time-Travel Debugging

```python
def replay_agent_history(initial_state, history):
    """Replay an agent's decisions for debugging"""
    state = initial_state
    for action, recorded_state in history:
        print(f"State: {recorded_state}")
        print(f"Action: {action}")
        state = interpret_action(action, state)
        print(f"New State: {state}\n")
    return state

def rewind_to_decision(state, steps_back):
    """Go back N decisions"""
    if steps_back > len(state.history):
        return None
    
    # Get the historical state
    _, historical_state = state.history[-steps_back]
    return historical_state.copy()
```

#### Parallel Universe Exploration

```python
def explore_outcomes(state, behavior, depth=3):
    """Explore possible futures to find best action"""
    if depth == 0:
        return evaluate_state(state), []
    
    # Get all possible actions at this state
    possible_actions = generate_possible_actions(state)
    
    best_score = float('-inf')
    best_path = []
    
    for action in possible_actions:
        new_state = interpret_action(action, state)
        score, future_path = explore_outcomes(new_state, behavior, depth - 1)
        
        if score > best_score:
            best_score = score
            best_path = [action] + future_path
    
    return best_score, best_path

def planning_behavior(base_behavior):
    """Enhance behavior with look-ahead planning"""
    def enhanced(state):
        # Look ahead to find best action
        _, best_path = explore_outcomes(state, base_behavior)
        return best_path[0] if best_path else make_action('wait')
    return enhanced
```

#### Behavior Learning

```python
class AdaptiveBehavior:
    def __init__(self, behaviors):
        self.behaviors = behaviors
        self.weights = {b: 1.0 for b in behaviors}
        self.recent_outcomes = []
    
    def __call__(self, state):
        # Choose behavior based on learned weights
        behavior = self.weighted_choice()
        action = behavior(state)
        
        # Record for learning
        self.recent_outcomes.append((behavior, state, action))
        
        return action
    
    def update_weights(self, reward):
        """Adjust weights based on outcomes"""
        for behavior, state, action in self.recent_outcomes[-10:]:
            self.weights[behavior] *= (1 + reward * 0.1)
        
        # Normalize weights
        total = sum(self.weights.values())
        self.weights = {b: w/total for b, w in self.weights.items()}
```

## Implementation Roadmap

### Phase 1: Core System (1-2 weeks)
- Implement basic actions and state
- Create simple behaviors
- Build action interpreter
- Test with basic agents

### Phase 2: Composition Tools (1-2 weeks)
- Priority, conditional, and weighted composers
- Behavior testing framework
- Performance profiling
- Debug visualization

### Phase 3: Graph System (2-3 weeks)
- Node and graph implementation
- Visual graph editor
- Graph execution engine
- Complex behavior examples

### Phase 4: Advanced Features (2-4 weeks)
- Time-travel debugging tools
- Parallel exploration (if needed)
- Learning behaviors
- Multi-agent coordination

## Key Advantages of This Approach

### 1. **Simplicity**
- Anyone can understand `state -> action`
- Debugging is straightforward
- No abstract concepts required

### 2. **Composability**
- Behaviors combine naturally
- Build complex from simple
- Reuse everywhere

### 3. **Performance**
- No abstraction overhead
- Direct function calls
- Easy to optimize hot paths

### 4. **Flexibility**
- Add features as needed
- Swap implementations
- No framework lock-in

### 5. **Testability**
- Pure functions are trivial to test
- Deterministic by default
- Can replay exact scenarios

## Comparison with Original Design

| Aspect | Monadic Design | Procedural Design |
|--------|---------------|-------------------|
| Learning Curve | Steep (monads, categories) | Gentle (functions, data) |
| Performance | Abstraction overhead | Direct and fast |
| Debugging | Complex stack traces | Clear execution flow |
| Team Adoption | Requires FP expertise | Familiar to all |
| Flexibility | Framework constraints | Complete freedom |
| Type Safety | Strong (in typed langs) | Runtime validation |

## Migration Path from Current Systems

1. **Wrap existing code** - Current AI can be behaviors
2. **Gradual adoption** - One agent type at a time
3. **Preserve interfaces** - Same API, new internals
4. **Benchmark everything** - Ensure performance gains

## Example: Complete Agent

```python
# Define an agent with all the pieces

# State sensing conditions
def low_health(state):
    return state.health < 30

def see_enemy(state):
    return any(e.type == 'enemy' for e in state.world_view.entities)

def has_potion(state):
    return 'health_potion' in state.inventory

# Basic behaviors
def heal_behavior(state):
    if has_potion(state):
        return make_action('use_item', item='health_potion')
    return None

# Composed behavior
survivor_agent = priority_behavior(
    conditional_behavior(low_health, heal_behavior, None),
    conditional_behavior(see_enemy, flee_behavior, explore_behavior)
)

# Or as a graph
survivor_graph = BehaviorGraph([
    BehaviorNode('explore', explore_behavior, {
        see_enemy: 'evaluate_threat',
        low_health: 'find_safety'
    }),
    BehaviorNode('evaluate_threat', evaluate_behavior, {
        threat_high: 'flee',
        threat_low: 'attack'
    }),
    BehaviorNode('flee', flee_behavior, {
        safe: 'explore'
    }),
    BehaviorNode('attack', attack_behavior, {
        enemy_dead: 'explore',
        low_health: 'flee'
    }),
    BehaviorNode('find_safety', heal_behavior, {
        healed: 'explore'
    })
], start_node='explore')

# Running the agent
def run_agent(agent, initial_state, steps=100):
    state = initial_state
    for _ in range(steps):
        action = agent(state)
        state = interpret_action(action, state)
        yield state, action
```

## Conclusion

This SICP-aligned design achieves all your original goals while remaining simple, clear, and performant. The key insight: **monads were solving problems you don't have yet**. This procedural approach gives you:

- ✅ Composable behaviors
- ✅ Time-travel debugging  
- ✅ Parallel exploration
- ✅ Data-driven design
- ✅ Visual node graphs

All without the conceptual overhead. You can always add monadic abstractions later if specific problems demand them, but start with what's simple and proven.