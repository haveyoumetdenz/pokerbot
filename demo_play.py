#!/usr/bin/env python3
"""
Demo script to show how the Deep CFR poker AI works.
This script demonstrates the AI playing poker without requiring user input.
"""

import pokers as pkrs
import torch
import numpy as np
import random
from src.core.deep_cfr import DeepCFRAgent
from src.core.model import set_verbose

def card_to_string(card):
    """Convert a poker card to a readable string."""
    suits = {0: "♣", 1: "♦", 2: "♥", 3: "♠"}
    ranks = {0: "2", 1: "3", 2: "4", 3: "5", 4: "6", 5: "7", 6: "8", 
             7: "9", 8: "10", 9: "J", 10: "Q", 11: "K", 12: "A"}
    
    return f"{ranks[int(card.rank)]}{suits[int(card.suit)]}"

def get_action_description(action):
    """Convert a pokers action to a human-readable string."""
    if action.action == pkrs.ActionEnum.Fold:
        return "Fold"
    elif action.action == pkrs.ActionEnum.Check:
        return "Check"
    elif action.action == pkrs.ActionEnum.Call:
        return f"Call ${action.amount:.2f}"
    elif action.action == pkrs.ActionEnum.Raise:
        return f"Raise to ${action.amount:.2f}"
    else:
        return f"Unknown action: {action.action}"

def display_game_state(state, stage_name):
    """Display the current game state."""
    print(f"\n{'='*60}")
    print(f"Stage: {stage_name}")
    print(f"Pot: ${state.pot:.2f}")
    print(f"Button position: Player {state.button}")
    
    # Show community cards
    if state.public_cards:
        community_str = " ".join([card_to_string(card) for card in state.public_cards])
        print(f"Community cards: {community_str}")
    else:
        print("Community cards: None")
    
    # Show player states
    print("\nPlayers:")
    for i, player in enumerate(state.players_state):
        status = "Active" if player.active else "Folded"
        print(f"Player {i}: ${player.stake:.2f} - Bet: ${player.bet_chips:.2f} - {status}")

def demo_ai_vs_ai():
    """Demonstrate AI vs AI gameplay to show how the system works."""
    print("🤖 Deep CFR Poker AI Demo")
    print("=" * 60)
    print("This demo shows how the Deep CFR AI plays poker.")
    print("We'll watch two AI agents play against each other.")
    print()
    
    # Load a trained model
    model_path = "models/checkpoint_iter_100.pt"
    print(f"Loading trained model: {model_path}")
    
    # Create AI agents
    ai_agent_1 = DeepCFRAgent(player_id=0, num_players=2, device='cpu')
    ai_agent_2 = DeepCFRAgent(player_id=1, num_players=2, device='cpu')
    
    # Load the trained model for agent 1
    try:
        ai_agent_1.load_model(model_path)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Could not load model: {e}")
        print("Using untrained agent instead.")
    
    # Create a 2-player poker game
    print("\n🎮 Starting 2-player poker game...")
    state = pkrs.State.from_seed(
        n_players=2,
        button=0,
        sb=1,
        bb=2,
        stake=200.0,
        seed=42
    )
    
    stage_names = {
        0: "PreFlop",
        1: "Flop", 
        2: "Turn", 
        3: "River", 
        4: "Showdown"
    }
    
    game_round = 1
    max_rounds = 10  # Limit to prevent infinite games
    
    while not state.final_state and game_round <= max_rounds:
        current_player = state.current_player
        stage_name = stage_names.get(int(state.stage), str(state.stage))
        
        # Show game state
        display_game_state(state, stage_name)
        
        # Get AI action
        if current_player == 0:
            action = ai_agent_1.choose_action(state)
            agent_name = "Deep CFR AI"
        else:
            action = ai_agent_2.choose_action(state)
            agent_name = "Random AI"
        
        print(f"\nPlayer {current_player} ({agent_name}) chose: {get_action_description(action)}")
        
        # Apply action
        new_state = state.apply_action(action)
        
        if new_state.status != pkrs.StateStatus.Ok:
            print(f"❌ Invalid action! Status: {new_state.status}")
            break
            
        state = new_state
        game_round += 1
        
        # Small delay to make it readable
        import time
        time.sleep(0.5)
    
    # Show final results
    print(f"\n{'='*60}")
    print("🏁 GAME OVER!")
    print(f"Final pot: ${state.pot:.2f}")
    
    for i, player in enumerate(state.players_state):
        if player.active:
            print(f"Player {i} (Winner): ${player.stake + player.pot_chips:.2f}")
        else:
            print(f"Player {i} (Folded): ${player.stake + player.pot_chips:.2f}")
    
    print("\n🎯 What you just saw:")
    print("• The Deep CFR AI making strategic decisions")
    print("• How the AI evaluates poker situations")
    print("• The difference between trained and random play")
    print("• Real-time poker gameplay with neural networks")

def demo_training_concepts():
    """Explain the key concepts behind Deep CFR."""
    print("\n" + "="*60)
    print("🧠 Deep CFR Concepts Explained")
    print("="*60)
    
    concepts = [
        ("🎯 Counterfactual Regret Minimization (CFR)", 
         "CFR is a game-theoretic algorithm that learns optimal strategies by minimizing 'regret' - the difference between what you could have won vs what you actually won."),
        
        ("🧠 Neural Networks", 
         "Instead of storing strategies in lookup tables (impossible for poker's huge state space), Deep CFR uses neural networks to approximate optimal strategies."),
        
        ("📊 Regret Calculation", 
         "For each action, the AI calculates: Regret = (Action Value) - (Expected Value). Positive regrets mean the action was better than average."),
        
        ("🎲 Strategy Computation", 
         "The AI uses 'regret matching' - it plays actions proportional to their positive regrets. This ensures it plays good actions more often."),
        
        ("🔄 Self-Improvement", 
         "Over many iterations, the AI accumulates regrets, updates its neural networks, and gradually improves its strategy."),
        
        ("🎮 State Representation", 
         "The AI sees poker as a 500-dimensional vector encoding: cards, pot size, positions, player states, legal actions, etc."),
        
        ("⚡ Continuous Bet Sizing", 
         "Unlike traditional poker bots with fixed bet sizes, this AI predicts bet amounts as fractions of the pot (0.1x to 3x pot)."),
        
        ("🎯 Opponent Modeling", 
         "Advanced versions track opponent behavior patterns and adapt strategy based on individual opponent tendencies.")
    ]
    
    for title, explanation in concepts:
        print(f"\n{title}")
        print(f"   {explanation}")

def demo_training_process():
    """Show what happens during training."""
    print("\n" + "="*60)
    print("🏋️ Training Process Explained")
    print("="*60)
    
    print("""
During training, the Deep CFR system:

1. 🎮 Game Tree Traversal
   • Simulates thousands of poker games
   • For each decision point, calculates counterfactual values
   • Stores experiences in prioritized memory buffers

2. 🧠 Neural Network Training
   • Advantage Network: Learns to predict regret values
   • Strategy Network: Learns optimal action probabilities
   • Uses prioritized experience replay for efficient learning

3. 📈 Strategy Improvement
   • Accumulates regrets over many iterations
   • Updates neural networks based on regret data
   • Gradually converges to Nash equilibrium strategies

4. 🎯 Evaluation
   • Tests performance against random opponents
   • Measures profit/loss to track learning progress
   • Saves checkpoints for continued training

The result: An AI that learns to play poker at a superhuman level!
""")

if __name__ == "__main__":
    # Set up the environment
    set_verbose(False)  # Reduce output noise
    
    print("🎯 Welcome to the Deep CFR Poker AI Demo!")
    print("This demo will show you how the AI works and learns to play poker.")
    print()
    
    # Run the demo
    demo_ai_vs_ai()
    demo_training_concepts()
    demo_training_process()
    
    print("\n" + "="*60)
    print("🎉 Demo Complete!")
    print("="*60)
    print("You now understand how Deep CFR works!")
    print("\nNext steps:")
    print("• Run longer training: python -m src.training.train --iterations 1000")
    print("• Try advanced training: python -m src.training.train --mixed")
    print("• Play against AI: python -m scripts.play --models-dir models")
    print("• Monitor training: Open http://localhost:6006 in your browser")

