#!/usr/bin/env python3
"""
Test script to debug betting history tracking.
"""

import pokers as pkrs
import random
from src.interpretable.interpretable_agent import InterpretablePokerAgent
from src.agents.strategic_agent import StrategicAgent

def test_betting_history():
    """Test if betting history is tracking opponents."""
    
    print("=" * 70)
    print("Testing Betting History Tracking")
    print("=" * 70)
    
    # Create interpretable agent
    agent = InterpretablePokerAgent(player_id=0, tree_dir='interpretable_output/models/models')
    
    # Enable debug mode
    agent._debug_betting_history = True
    
    print(f"Agent player_id: {agent.player_id}")
    print(f"Initial betting history: {len(agent.betting_history['opponent_stats'])} opponents")
    
    # Create opponents
    opponents = [StrategicAgent(i, tightness='average') for i in range(1, 6)]
    agents = [agent] + opponents
    
    # Start new game
    agent.start_new_game()
    print(f"After start_new_game: {agent.betting_history['game_count']} games")
    
    # Create a game
    state = pkrs.State.from_seed(
        n_players=6,
        button=0,
        sb=1,
        bb=2,
        stake=200.0,
        seed=42
    )
    
    round_num = 0
    actions_recorded = 0
    
    print("\nPlaying game...")
    while not state.final_state and round_num < 20:  # Limit rounds for testing
        current_player = state.current_player
        round_num += 1
        
        # Get action
        action = agents[current_player].choose_action(state)
        
        # Record opponent actions
        if current_player != 0:
            print(f"  Round {round_num}: Player {current_player} action: {action.action}")
            try:
                agent.record_action(state, current_player, action)
                actions_recorded += 1
                print(f"    ✓ Recorded action for player {current_player}")
                
                # Check if opponent was tracked
                if current_player in agent.betting_history['opponent_stats']:
                    stats = agent.betting_history['opponent_stats'][current_player]
                    print(f"    ✓ Opponent {current_player} stats: {stats['total_actions']} actions")
                else:
                    print(f"    ✗ Opponent {current_player} NOT in stats!")
            except Exception as e:
                print(f"    ✗ Error recording action: {e}")
                import traceback
                traceback.print_exc()
        
        # Apply action
        new_state = state.apply_action(action)
        if new_state.status != pkrs.StateStatus.Ok:
            print(f"  ⚠️  Invalid action! Status: {new_state.status}")
            break
        
        state = new_state
    
    print(f"\nGame finished after {round_num} rounds")
    print(f"Actions recorded: {actions_recorded}")
    print(f"Opponents tracked: {len(agent.betting_history['opponent_stats'])}")
    
    if agent.betting_history['opponent_stats']:
        print("\nOpponent Statistics:")
        for opp_id, stats in agent.betting_history['opponent_stats'].items():
            print(f"  Player {opp_id}:")
            print(f"    Total actions: {stats['total_actions']}")
            print(f"    Raises: {stats['raises']}, Calls: {stats['calls']}, Folds: {stats['folds']}")
            print(f"    Aggression factor: {stats['aggression_factor']:.2f}")
    else:
        print("\n❌ NO OPPONENTS TRACKED!")
        print("This is the problem - betting history isn't working.")
    
    # Check betting history features
    print("\nTesting feature extraction with betting history...")
    features = agent._get_features(state) if hasattr(agent, '_get_features') else None
    
    if features:
        print("Betting history features:")
        bh_features = [
            'street_raise_frequency', 'street_call_frequency', 'street_fold_frequency',
            'avg_opponent_raise_frequency', 'avg_opponent_call_frequency',
            'avg_opponent_aggression', 'avg_opponent_vpip', 'avg_opponent_pfr',
            'games_played'
        ]
        for feat in bh_features:
            if feat in features:
                print(f"  {feat}: {features[feat]}")
            else:
                print(f"  {feat}: NOT FOUND")

if __name__ == "__main__":
    test_betting_history()

