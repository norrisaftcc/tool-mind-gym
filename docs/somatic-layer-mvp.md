# Somatic Layer MVP with Map/Reduce Temporal Sync

## Map/Reduce for Temporal Synchronization

```python
from pocketflow import Node, Flow
import asyncio
from collections import deque
from dataclasses import dataclass
import numpy as np

@dataclass
class SomaticState:
    """Minimal somatic tracking"""
    arousal: float = 0.5      # 0=low, 1=high
    valence: float = 0.0      # -1=negative, +1=positive  
    coherence: float = 0.5    # 0=scattered, 1=focused
    pressure: float = 0.0     # 0=relaxed, 1=urgent
    
    def to_vector(self):
        return np.array([self.arousal, self.valence, self.coherence, self.pressure])
    
    def stress_level(self):
        # High arousal + negative valence + low coherence = stress
        return self.arousal * (1 - self.valence) / 2 * (1 - self.coherence)

class IntuitiveMapNode(Node):
    """Maps query to multiple rapid intuitive responses"""
    def __init__(self):
        self.burst_size = 10  # Generate 10 quick thoughts
        
    def exec(self, query):
        # Rapid-fire intuitive responses (50-100ms each)
        intuitions = []
        for i in range(self.burst_size):
            thought = call_local_llm(
                f"Quick intuitive response #{i+1} to: {query}\n"
                f"(One short phrase only):",
                max_tokens=20,
                temperature=0.9 - (i * 0.05)  # Decreasing temperature
            )
            intuitions.append({
                "content": thought,
                "timestamp": time.time(),
                "confidence": np.random.beta(2, 5)  # Skewed low
            })
        return intuitions
    
    def post(self, shared, prep_res, exec_res):
        shared["intuitive_burst"] = exec_res
        # Update somatic state from burst
        variance = np.var([t["confidence"] for t in exec_res])
        shared["somatic"].coherence = 1.0 - variance
        return "reduce"

class SomaticReduceNode(Node):
    """Reduces intuitive burst considering somatic state"""
    def prep(self, shared):
        return {
            "burst": shared["intuitive_burst"],
            "somatic": shared["somatic"]
        }
    
    def exec(self, context):
        burst = context["burst"]
        somatic = context["somatic"]
        
        # Somatic state influences reduction strategy
        if somatic.stress_level() > 0.7:
            # High stress: pick most confident/safe
            selected = max(burst, key=lambda x: x["confidence"])
            strategy = "conservative"
        elif somatic.arousal < 0.3:
            # Low arousal: pick most novel/interesting
            selected = min(burst, key=lambda x: x["confidence"])
            strategy = "exploratory"
        else:
            # Balanced: weighted clustering
            clusters = self.cluster_thoughts(burst)
            selected = self.pick_representative(clusters)
            strategy = "balanced"
            
        return {
            "selected_thoughts": selected,
            "strategy": strategy,
            "reduced_from": len(burst)
        }
    
    def post(self, shared, prep_res, exec_res):
        shared["intuitive_summary"] = exec_res
        # Update arousal based on reduction
        reduction_ratio = len(exec_res["selected_thoughts"]) / exec_res["reduced_from"]
        shared["somatic"].arousal *= (1 + reduction_ratio)
        shared["somatic"].arousal = min(1.0, shared["somatic"].arousal)
        return "analytical"

class AnalyticalMapNode(Node):
    """Maps reduced intuitions to analytical examination"""
    def exec(self, intuitive_summary):
        # Slower, deeper analysis of selected intuitions
        analyses = []
        for thought in intuitive_summary["selected_thoughts"]:
            analysis = call_api_llm(
                f"Analytically examine this intuition: {thought['content']}\n"
                f"Consider logical consistency, evidence, and implications:",
                max_tokens=200
            )
            analyses.append({
                "intuition": thought,
                "analysis": analysis,
                "timestamp": time.time()
            })
        return analyses
    
    def post(self, shared, prep_res, exec_res):
        shared["analytical_burst"] = exec_res
        # Analytical process calms arousal
        shared["somatic"].arousal *= 0.8
        return "somatic_integration"

class SomaticIntegrationNode(Node):
    """Integrates cognitive and somatic information"""
    def exec(self, shared):
        somatic = shared["somatic"]
        
        # Calculate valence from thought content
        positive_signals = count_positive_indicators(shared)
        negative_signals = count_negative_indicators(shared)
        somatic.valence = (positive_signals - negative_signals) / (positive_signals + negative_signals + 1)
        
        # Coherence from agreement between hemispheres
        agreement = calculate_hemisphere_agreement(
            shared["intuitive_summary"],
            shared["analytical_burst"]
        )
        somatic.coherence = somatic.coherence * 0.7 + agreement * 0.3
        
        # Pressure from external factors
        if shared.get("deadline_approaching"):
            somatic.pressure = min(1.0, somatic.pressure + 0.2)
        else:
            somatic.pressure *= 0.9
            
        # Update PNG based on somatic state
        self.update_png_from_somatic(shared["png_state"], somatic)
        
        return {
            "integrated_state": somatic,
            "action_recommendation": self.recommend_action(somatic)
        }
    
    def recommend_action(self, somatic):
        if somatic.stress_level() > 0.8:
            return "pause_and_breathe"
        elif somatic.coherence < 0.3:
            return "need_more_thinking"
        elif somatic.arousal > 0.9:
            return "discharge_through_action"
        else:
            return "proceed_normally"
    
    def update_png_from_somatic(self, png_state, somatic):
        """Somatic state influences PNG evolution rules"""
        # High arousal = faster evolution
        png_state.evolution_rate = 1 + (somatic.arousal * 2)
        
        # Low coherence = more random noise
        if somatic.coherence < 0.5:
            noise_level = (0.5 - somatic.coherence) * 0.2
            png_state.add_noise(noise_level)
        
        # Negative valence = decay patterns
        if somatic.valence < -0.3:
            png_state.decay_rate = abs(somatic.valence)
```

## Dream State Serialization

```python
import git
import pickle
import json
from datetime import datetime

class DreamStateManager:
    """Manages dream states as git branches"""
    
    def __init__(self, repo_path="./agent_dreams"):
        self.repo_path = repo_path
        self.repo = git.Repo.init(repo_path)
        
    def save_conscious_state(self, shared_state, tag=None):
        """Commit current state before dreaming"""
        timestamp = datetime.now().isoformat()
        
        # Serialize different components
        state_files = {
            "somatic.json": json.dumps(asdict(shared_state["somatic"])),
            "png_state.npy": shared_state["png_state"].grid,
            "memory_buffer.pkl": pickle.dumps(shared_state["memory_buffer"]),
            "thought_history.jsonl": "\n".join(
                json.dumps(t) for t in shared_state["thought_history"]
            )
        }
        
        # Write files
        for filename, content in state_files.items():
            path = os.path.join(self.repo_path, filename)
            if filename.endswith('.npy'):
                np.save(path, content)
            elif filename.endswith('.pkl'):
                with open(path, 'wb') as f:
                    f.write(content)
            else:
                with open(path, 'w') as f:
                    f.write(content)
        
        # Commit
        self.repo.index.add(list(state_files.keys()))
        commit = self.repo.index.commit(f"Conscious state: {timestamp}")
        
        if tag:
            self.repo.create_tag(tag, ref=commit)
            
        return commit.hexsha
    
    def begin_dream_cycle(self, base_commit):
        """Create new branch for dreaming"""
        dream_branch = f"dream_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.repo.create_head(dream_branch, commit=base_commit)
        self.repo.head.reference = self.repo.heads[dream_branch]
        return dream_branch
    
    def save_dream_checkpoint(self, dream_state, message):
        """Save intermediate dream state"""
        # Similar to save_conscious_state but on dream branch
        # Commits represent dream evolution
        pass
    
    def wake_up(self, dream_branch, conscious_branch="main"):
        """Merge useful dream discoveries back"""
        # Evaluate dream branch
        dream_value = self.evaluate_dream_branch(dream_branch)
        
        if dream_value > 0.7:
            # Valuable dream - merge back
            self.repo.head.reference = self.repo.heads[conscious_branch]
            self.repo.index.merge_tree(self.repo.heads[dream_branch])
            self.repo.index.commit(f"Integrated dream: {dream_branch}")
        else:
            # Forgettable dream - just switch back
            self.repo.head.reference = self.repo.heads[conscious_branch]
            
        # Optionally keep dream branch for analysis
        return dream_value
```

## MVP Somatic Feedback Loop

```python
class SomaticFeedbackNode(Node):
    """Minimal somatic layer that modulates thinking"""
    
    def __init__(self):
        self.history = deque(maxlen=100)
        self.baseline = SomaticState()
        
    def exec(self, shared):
        current = shared["somatic"]
        
        # Simple feedback rules
        if current.stress_level() > 0.7:
            # Stress response: simplify
            shared["max_dialogue_rounds"] = 1
            shared["temperature"] = 0.3
            shared["intuitive_burst_size"] = 3
            
        elif current.arousal < 0.3 and current.coherence > 0.7:
            # Bored but focused: explore
            shared["max_dialogue_rounds"] = 5
            shared["temperature"] = 0.9
            shared["intuitive_burst_size"] = 20
            
        else:
            # Normal operation
            shared["max_dialogue_rounds"] = 3
            shared["temperature"] = 0.7
            shared["intuitive_burst_size"] = 10
            
        # Record for pattern detection
        self.history.append({
            "state": current,
            "params": {
                "rounds": shared["max_dialogue_rounds"],
                "temp": shared["temperature"],
                "burst": shared["intuitive_burst_size"]
            },
            "timestamp": time.time()
        })
        
        return shared
```

## Why This Works

1. **Map/Reduce handles the temporal mismatch perfectly**:
   - Map: Generate many fast intuitions in parallel
   - Reduce: Compress based on somatic state
   - This mirrors how the brain consolidates microsaccades into perception

2. **Somatic state as a control signal**:
   - Not just monitoring but actively modulating
   - Stress → conservative reduction
   - Calm → exploratory reduction
   - This prevents both anxiety spirals and getting stuck

3. **Git-based dreaming is brilliant because**:
   - Dreams are literally alternate timelines
   - Can explore without commitment
   - Valuable insights can be merged back
   - Failed dreams just get garbage collected
   - Perfect for the "geologic pace" of deep thinking

The key insight: The somatic layer isn't just feeling, it's the **governor** that prevents the engine from redlining or stalling.