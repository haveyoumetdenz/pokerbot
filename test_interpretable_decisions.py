#!/usr/bin/env python3
"""
Simple test script to show interpretable poker AI decision explanations.
"""

import os
import sys
import pokers as pkrs

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from src.interpretable.interpretable_agent import InterpretablePokerAgent

def test_interpretable_decisions():
    """Test the interpretable agent and show decision explanations."""
    
    print("🎯 Testing Interpretable Poker AI Decision Explanations")
    print("=" * 60)
    
    # Create interpretable agent
    agent = InterpretablePokerAgent(player_id=0, tree_dir='interpretable_output/models')
    
    # Test different game scenarios
    scenarios = [
        {"name": "Preflop Scenario", "stage": 0, "seed": 42},
        {"name": "Flop Scenario", "stage": 1, "seed": 123},
        {"name": "Turn Scenario", "stage": 2, "seed": 456},
        {"name": "River Scenario", "stage": 3, "seed": 789}
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🎮 Scenario {i}: {scenario['name']}")
        print("-" * 40)
        
        # Create game state
        state = pkrs.State.from_seed(
            n_players=6, 
            button=0, 
            sb=1, 
            bb=2, 
            stake=200.0, 
            seed=scenario['seed']
        )
        
        # Note: We'll use different seeds to get different stages naturally
        # The stage will be determined by the game progression
        
        # Get decision explanation
        explanation = agent.explain_decision(state)
        
        # Display results
        print(f"Action: {explanation['action'].upper()}")
        print(f"Confidence: {explanation['confidence']:.1%}")
        print(f"Action Probabilities:")
        for action, prob in explanation['probabilities'].items():
            print(f"  {action.upper()}: {prob:.1%}")
        
        print(f"\nExplanation:")
        print(f"  {explanation['explanation']}")
        
        # Show key features
        features = explanation['features']
        print(f"\nKey Features:")
        print(f"  Hand Equity: {features.get('hand_equity', 0):.1%}")
        print(f"  Pot Odds: {features.get('pot_odds', 0):.1%}")
        print(f"  Position: {features.get('position', 'unknown')}")
        print(f"  Pot Size: {features.get('pot_size_bb', 0):.1f} BB")
        print(f"  Stack Size: {features.get('stack_size_bb', 0):.1f} BB")

if __name__ == "__main__":
    test_interpretable_decisions()
