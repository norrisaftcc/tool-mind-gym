#!/usr/bin/env python3
"""
Mind Gym Brutal MVP - Prove the bicameral concept works
Single file, <300 lines, no frameworks needed
"""

import asyncio
import time
import random
from typing import List, Dict, AsyncIterator
from dataclasses import dataclass
import os
import json

# You can use OpenAI or Anthropic - just set your API key
try:
    import anthropic
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None
except ImportError:
    client = None
    print("Warning: Anthropic not installed. Using mock mode.")

# --- Somatic State (Emotional Governor) ---
@dataclass
class SomaticState:
    """Tracks emotional/cognitive load"""
    arousal: float = 0.5      # 0=calm, 1=activated  
    valence: float = 0.0      # -1=negative, +1=positive
    coherence: float = 0.5    # 0=confused, 1=clear
    tension: float = 0.0      # 0=relaxed, 1=strained
    
    def stress_level(self) -> float:
        """Combined stress metric"""
        return (self.arousal * (1 - self.valence) / 2) * (1 - self.coherence)
    
    def update_from_thought(self, thought: str):
        """Adjust state based on thought content"""
        # Simple heuristics - in real version this would be more sophisticated
        if "confused" in thought.lower() or "uncertain" in thought.lower():
            self.coherence *= 0.9
            self.arousal += 0.1
        if "clear" in thought.lower() or "understand" in thought.lower():
            self.coherence = min(1.0, self.coherence * 1.1)
        if "!" in thought:
            self.arousal = min(1.0, self.arousal + 0.05)
        
        # Tension increases over time
        self.tension = min(1.0, self.tension + 0.02)
    
    def needs_rest(self) -> bool:
        """Should we trigger a rest state?"""
        return self.stress_level() > 0.8 or self.tension > 0.9

# --- The Two Minds ---
class IntuitiveMind:
    """Fast, associative, creative - runs on local model (or simulated)"""
    
    async def think(self, query: str, somatic: SomaticState) -> List[str]:
        """Generate quick intuitive bursts"""
        # In real version: use local LLM
        # For MVP: simulate or use API with different prompt
        
        burst_size = 3 if somatic.stress_level() < 0.5 else 2
        
        thoughts = []
        for i in range(burst_size):
            if client:
                # Real API call with intuitive prompt
                prompt = f"""You are the intuitive, creative hemisphere of a bicameral mind.
                Respond with a brief, associative, creative thought about: {query}
                Be instinctive, pattern-based, use metaphors. Keep it under 50 words.
                Thought {i+1} of {burst_size}:"""
                
                response = client.messages.create(
                    model="claude-3-haiku-20240307",  # Faster model for intuitive
                    max_tokens=100,
                    temperature=0.9,  # Higher temperature for creativity
                    messages=[{"role": "user", "content": prompt}]
                )
                thoughts.append(response.content[0].text)
            else:
                # Mock mode
                associations = [
                    f"Pattern: {query} reminds me of flowing water...",
                    f"Feeling: There's something rhythmic about {query}",
                    f"Image: Like a spiral unfolding from {query}",
                    f"Instinct: {query} wants to become something else"
                ]
                thoughts.append(random.choice(associations))
            
            await asyncio.sleep(0.1)  # Fast bursts
        
        return thoughts

class AnalyticalMind:
    """Slow, logical, structured - runs on API model"""
    
    async def think(self, query: str, intuitive_thoughts: List[str], somatic: SomaticState) -> str:
        """Deep analytical processing"""
        if client:
            # Real API call with analytical prompt
            prompt = f"""You are the analytical, logical hemisphere of a bicameral mind.
            
            Query: {query}
            
            Your intuitive hemisphere produced these thoughts:
            {chr(10).join(f'- {t}' for t in intuitive_thoughts)}
            
            Provide a structured, logical analysis. Consider the intuitive inputs but apply reasoning.
            Be systematic and thorough. 100-150 words."""
            
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",  # Stronger model for analysis
                max_tokens=200,
                temperature=0.3 if somatic.stress_level() > 0.7 else 0.5,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        else:
            # Mock mode
            return f"Analyzing '{query}': The intuitive insights suggest patterns of transformation and flow. Logically, this indicates a system in transition, seeking equilibrium through dynamic adjustment."

# --- Bicameral Dialogue Node ---
class DialogueNode:
    """Internal conversation between the two minds"""
    
    async def converse(self, intuitive_thoughts: List[str], analytical_thought: str, 
                       query: str, rounds: int = 2) -> List[Dict]:
        """Generate internal dialogue"""
        dialogue = []
        
        for round_num in range(rounds):
            if client:
                # Real dialogue using API
                prompt = f"""You are moderating an internal dialogue in a bicameral mind.
                
                Original query: {query}
                
                Intuitive mind said: {intuitive_thoughts[-1]}
                Analytical mind said: {analytical_thought if round_num == 0 else dialogue[-1]['content']}
                
                Generate a brief exchange where they challenge or build on each other's ideas.
                Round {round_num + 1} of {rounds}. Keep each response under 75 words.
                
                Format as dialogue between INTUITIVE and ANALYTICAL."""
                
                response = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=150,
                    temperature=0.6,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # Parse dialogue from response
                text = response.content[0].text
                if "INTUITIVE:" in text and "ANALYTICAL:" in text:
                    parts = text.split("ANALYTICAL:")
                    intuitive_part = parts[0].replace("INTUITIVE:", "").strip()
                    analytical_part = parts[1].strip() if len(parts) > 1 else ""
                    
                    dialogue.append({"speaker": "intuitive", "content": intuitive_part})
                    dialogue.append({"speaker": "analytical", "content": analytical_part})
                else:
                    dialogue.append({"speaker": "dialogue", "content": text})
            else:
                # Mock dialogue
                dialogue.extend([
                    {"speaker": "intuitive", "content": f"But what if {query} is more fluid than that?"},
                    {"speaker": "analytical", "content": f"Fluidity implies structure at a different scale."}
                ])
            
            await asyncio.sleep(0.5)
        
        return dialogue

# --- Synthesis Node ---
async def synthesize(query: str, intuitive: List[str], analytical: str, 
                     dialogue: List[Dict], somatic: SomaticState) -> str:
    """Final integration of both perspectives"""
    if client:
        prompt = f"""You are synthesizing a bicameral mind's thinking process.
        
        Query: {query}
        
        Intuitive insights:
        {chr(10).join(f'- {t}' for t in intuitive)}
        
        Analytical perspective:
        {analytical}
        
        Internal dialogue:
        {chr(10).join(f"{d['speaker']}: {d['content']}" for d in dialogue[-2:])}
        
        Current cognitive state:
        - Stress: {somatic.stress_level():.2f}
        - Coherence: {somatic.coherence:.2f}
        - Tension: {somatic.tension:.2f}
        
        Create a unified synthesis that honors both perspectives.
        Be insightful and integrative. 100-150 words."""
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=200,
            temperature=0.4,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    else:
        return f"Synthesis: Both the flowing, intuitive sense of {query} and its structural analysis reveal a dynamic system seeking balance through continuous adaptation."

# --- Main Mind Gym Class ---
class MindGym:
    """The complete bicameral thinking system"""
    
    def __init__(self):
        self.intuitive = IntuitiveMind()
        self.analytical = AnalyticalMind()
        self.dialogue = DialogueNode()
        self.somatic = SomaticState()
        self.thought_history = []
    
    async def think(self, query: str) -> AsyncIterator[Dict]:
        """Complete thinking process with streaming output"""
        print(f"\n🧠 Mind Gym: Processing '{query}'\n")
        start_time = time.time()
        
        # Reset somatic state for new query
        self.somatic = SomaticState()
        
        # Phase 1: Intuitive burst
        yield {"phase": "intuitive", "status": "starting"}
        intuitive_thoughts = await self.intuitive.think(query, self.somatic)
        
        for thought in intuitive_thoughts:
            self.somatic.update_from_thought(thought)
            yield {
                "phase": "intuitive",
                "thought": thought,
                "somatic": {
                    "stress": self.somatic.stress_level(),
                    "coherence": self.somatic.coherence
                }
            }
        
        # Phase 2: Analytical processing
        yield {"phase": "analytical", "status": "starting"}
        analytical_thought = await self.analytical.think(query, intuitive_thoughts, self.somatic)
        self.somatic.update_from_thought(analytical_thought)
        
        yield {
            "phase": "analytical",
            "thought": analytical_thought,
            "somatic": {
                "stress": self.somatic.stress_level(),
                "tension": self.somatic.tension
            }
        }
        
        # Phase 3: Internal dialogue
        yield {"phase": "dialogue", "status": "starting"}
        dialogue_rounds = 1 if self.somatic.stress_level() > 0.7 else 2
        dialogue = await self.dialogue.converse(
            intuitive_thoughts, analytical_thought, query, dialogue_rounds
        )
        
        for exchange in dialogue:
            self.somatic.update_from_thought(exchange["content"])
            yield {
                "phase": "dialogue",
                "speaker": exchange["speaker"],
                "thought": exchange["content"],
                "somatic": {"coherence": self.somatic.coherence}
            }
        
        # Phase 4: Synthesis
        yield {"phase": "synthesis", "status": "starting"}
        synthesis = await synthesize(
            query, intuitive_thoughts, analytical_thought, dialogue, self.somatic
        )
        
        elapsed = time.time() - start_time
        
        yield {
            "phase": "complete",
            "synthesis": synthesis,
            "metrics": {
                "time": f"{elapsed:.1f}s",
                "stress_final": self.somatic.stress_level(),
                "coherence_final": self.somatic.coherence,
                "needs_rest": self.somatic.needs_rest()
            }
        }

# --- CLI Interface ---
async def main():
    """Run the Mind Gym from command line"""
    print("=" * 60)
    print("🧠💪 MIND GYM - Brutal MVP")
    print("=" * 60)
    print("\nThis is a bicameral AI that thinks through internal dialogue.")
    print("Watch as intuitive and analytical minds work together.\n")
    
    gym = MindGym()
    
    # Test queries of increasing complexity
    test_queries = [
        "What is happiness?",
        "How does consciousness emerge?",
        "Design a new musical instrument",
    ]
    
    print("Choose a query or enter your own:")
    for i, q in enumerate(test_queries, 1):
        print(f"{i}. {q}")
    print("4. Enter custom query")
    
    choice = input("\nChoice (1-4): ").strip()
    
    if choice in ["1", "2", "3"]:
        query = test_queries[int(choice) - 1]
    else:
        query = input("Enter your query: ").strip()
    
    # Process the query
    async for output in gym.think(query):
        if output.get("phase") == "intuitive" and "thought" in output:
            print(f"💭 [Intuitive]: {output['thought']}")
            print(f"   ↳ Stress: {'▓' * int(output['somatic']['stress'] * 10)}")
        
        elif output.get("phase") == "analytical" and "thought" in output:
            print(f"\n🔍 [Analytical]: {output['thought']}")
            print(f"   ↳ Tension: {'▓' * int(output['somatic']['tension'] * 10)}")
        
        elif output.get("phase") == "dialogue" and "thought" in output:
            speaker = "💭" if output["speaker"] == "intuitive" else "🔍"
            print(f"\n{speaker} [{output['speaker'].title()}]: {output['thought']}")
        
        elif output.get("phase") == "complete":
            print("\n" + "=" * 60)
            print("✨ SYNTHESIS:")
            print(output["synthesis"])
            print("\n" + "-" * 60)
            print(f"⏱️  Time: {output['metrics']['time']}")
            print(f"😰 Final stress: {output['metrics']['stress_final']:.2%}")
            print(f"🎯 Coherence: {output['metrics']['coherence_final']:.2%}")
            if output['metrics']['needs_rest']:
                print("💤 System needs rest!")

if __name__ == "__main__":
    asyncio.run(main())