#!/usr/bin/env python3
"""
Demo script to run the interpretable poker AI standalone.
Shows the interpretable agent playing games with full decision explanations.
"""

import os
import sys
import pokers as pkrs
import random
import argparse
from src.interpretable.interpretable_agent import InterpretablePokerAgent
from src.agents.random_agent import RandomAgent
from src.agents.strategic_agent import StrategicAgent

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

def display_game_state(state, player_id=None):
    """Display the current game state."""
    stage_names = {
        0: "PreFlop",
        1: "Flop", 
        2: "Turn", 
        3: "River", 
        4: "Showdown"
    }
    stage_name = stage_names.get(int(state.stage), str(state.stage))
    
    print(f"\n{'='*70}")
    print(f"Stage: {stage_name}")
    print(f"Pot: ${state.pot:.2f}")
    print(f"Button position: Player {state.button}")
    
    # Show community cards
    if state.public_cards:
        community_str = " ".join([card_to_string(card) for card in state.public_cards])
        print(f"Community cards: {community_str}")
    else:
        print("Community cards: None")
    
    # Show interpretable agent's cards if player_id is provided
    if player_id is not None and player_id < len(state.players_state):
        player = state.players_state[player_id]
        if player.active and hasattr(player, 'hand') and player.hand:
            hand_str = " ".join([card_to_string(card) for card in player.hand])
            print(f"\n🤖 Interpretable Agent's Hand: {hand_str}")
    
    # Show player states
    print("\nPlayers:")
    for i, player in enumerate(state.players_state):
        status = "Active" if player.active else "Folded"
        player_type = "[Interpretable Agent]" if i == player_id else "[Opponent]"
        print(f"Player {i} {player_type}: ${player.stake:.2f} - Bet: ${player.bet_chips:.2f} - {status}")

def run_interpretable_demo(num_games=3, tree_dir='interpretable_output/models/models', 
                          show_explanations=True, show_all_players=False,
                          opponent_type='strategic', opponent_tightness='average'):
    """Run interpretable agent playing games with explanations."""
    
    print("🤖 Interpretable Poker AI Demo")
    print("=" * 70)
    print("Watching the interpretable agent play poker with full explanations.")
    print(f"Tree directory: {tree_dir}")
    print(f"Opponent type: {opponent_type}")
    if opponent_type == 'strategic':
        print(f"Opponent tightness: {opponent_tightness}")
    print()
    
    # Load interpretable agent
    try:
        interpretable_agent = InterpretablePokerAgent(player_id=0, tree_dir=tree_dir)
        print("✅ Interpretable agent loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading interpretable agent: {e}")
        print(f"   Make sure tree files (.pkl) exist in: {tree_dir}")
        return
    
    # Track statistics
    total_profit = 0
    wins = 0
    
    for game_num in range(1, num_games + 1):
        print(f"\n{'#'*70}")
        print(f"# GAME {game_num}/{num_games}")
        print(f"{'#'*70}")
        
        # Create opponents based on type
        if opponent_type == 'strategic':
            opponents = [StrategicAgent(i, tightness=opponent_tightness) for i in range(1, 6)]
        else:
            opponents = [RandomAgent(i) for i in range(1, 6)]
        agents = [interpretable_agent] + opponents
        
        # Start new game for betting history tracking
        interpretable_agent.start_new_game()
        
        # Create a new game
        state = pkrs.State.from_seed(
            n_players=6,
            button=(game_num - 1) % 6,
            sb=1,
            bb=2,
            stake=200.0,
            seed=random.randint(0, 10000)
        )
        
        round_num = 0
        max_rounds = 100  # Safety limit
        
        while not state.final_state and round_num < max_rounds:
            current_player = state.current_player
            round_num += 1
            
            # Display state when interpretable agent acts
            if current_player == 0 or show_all_players:
                display_game_state(state, player_id=0)
            
            # Get action
            action = agents[current_player].choose_action(state)
            
            # Record action for betting history (for all players)
            # The interpretable agent records its own action in choose_action,
            # but we need to record opponent actions here
            if current_player != 0:
                interpretable_agent.record_action(state, current_player, action)
            
            # Show interpretable agent's decision with explanation
            if current_player == 0 and show_explanations:
                explanation = interpretable_agent.explain_decision(state)
                
                print(f"\n🧠 Interpretable Agent Decision:")
                print(f"  Action: {explanation['action'].upper()}")
                print(f"  Confidence: {explanation['confidence']:.1%}")
                print(f"  Action Probabilities:")
                for action_name, prob in explanation['probabilities'].items():
                    print(f"    {action_name.upper()}: {prob:.1%}")
                
                print(f"\n  Explanation:")
                print(f"    {explanation['explanation']}")
                
                print(f"\n  Key Features:")
                features = explanation['features']
                print(f"    Hand Equity: {features.get('hand_equity', 0):.1%}")
                print(f"    Pot Odds: {features.get('pot_odds', 0):.1%}")
                print(f"    Position: {features.get('position', 'unknown')}")
                print(f"    Pot Size: {features.get('pot_size_bb', 0):.1f} BB")
                print(f"    Stack Size: {features.get('stack_size_bb', 0):.1f} BB")
            else:
                # Show opponent actions briefly
                opponent_type_name = opponent_type.title() if opponent_type == 'strategic' else 'Random'
                print(f"\nPlayer {current_player} ({opponent_type_name}) chose: {get_action_description(action)}")
            
            # Apply action
            new_state = state.apply_action(action)
            
            if new_state.status != pkrs.StateStatus.Ok:
                print(f"❌ Invalid action! Status: {new_state.status}")
                break
            
            state = new_state
            
            # Small delay for readability
            import time
            time.sleep(0.3 if current_player == 0 else 0.1)
        
        # Show game results
        print(f"\n{'='*70}")
        print("🏁 GAME OVER!")
        print(f"Final pot: ${state.pot:.2f}")
        
        # Show final community cards
        if state.public_cards:
            community_str = " ".join([card_to_string(card) for card in state.public_cards])
            print(f"Final community cards: {community_str}")
        
        print("\nFinal hands:")
        for i, player in enumerate(state.players_state):
            if player.active:
                reward = player.reward
                status = "Winner" if reward > 0 else "Participant"
                # Show cards if available
                if hasattr(player, 'hand') and player.hand:
                    hand_str = " ".join([card_to_string(card) for card in player.hand])
                    player_type = "[Interpretable Agent]" if i == 0 else "[Random]"
                    print(f"Player {i} {player_type} ({status}): {hand_str} - ${player.stake + player.pot_chips:.2f} (profit: ${reward:.2f})")
                else:
                    print(f"Player {i} ({status}): ${player.stake + player.pot_chips:.2f} (profit: ${reward:.2f})")
            else:
                # Show folded players' cards if available
                if hasattr(player, 'hand') and player.hand:
                    hand_str = " ".join([card_to_string(card) for card in player.hand])
                    player_type = "[Interpretable Agent]" if i == 0 else "[Random]"
                    print(f"Player {i} {player_type} (Folded): {hand_str} - ${player.stake + player.pot_chips:.2f}")
                else:
                    print(f"Player {i} (Folded): ${player.stake + player.pot_chips:.2f}")
        
        # Track interpretable agent's performance
        interpretable_reward = state.players_state[0].reward
        total_profit += interpretable_reward
        if interpretable_reward > 0:
            wins += 1
        
        print(f"\n📊 Game {game_num} Summary:")
        print(f"  Interpretable Agent profit: ${interpretable_reward:.2f}")
        print(f"  {'Won!' if interpretable_reward > 0 else 'Lost' if interpretable_reward < 0 else 'Broke even'}")
    
    # Final statistics
    print(f"\n{'='*70}")
    print("📈 OVERALL STATISTICS")
    print(f"{'='*70}")
    print(f"Games played: {num_games}")
    print(f"Wins: {wins}/{num_games} ({wins/num_games*100:.1f}% win rate)")
    print(f"Total profit: ${total_profit:.2f}")
    print(f"Average profit per game: ${total_profit/num_games:.2f}")
    print(f"\n🎯 What you just saw:")
    print(f"  • Interpretable agent making decisions with explanations")
    print(f"  • Full transparency on why each decision was made")
    print(f"  • Decision trees in action (feature-based reasoning)")
    print(f"  • How interpretable AI plays poker")

def main():
    parser = argparse.ArgumentParser(description='Run interpretable poker AI demo')
    parser.add_argument('--tree-dir', type=str, default='interpretable_output/models/models',
                       help='Directory containing trained decision trees (.pkl files)')
    parser.add_argument('--num-games', type=int, default=3,
                       help='Number of games to play')
    parser.add_argument('--no-explanations', action='store_true',
                       help='Hide decision explanations (faster)')
    parser.add_argument('--show-all', action='store_true',
                       help='Show game state for all players, not just interpretable agent')
    parser.add_argument('--opponent-type', type=str, default='strategic',
                       choices=['random', 'strategic'],
                       help='Type of opponent: random or strategic (default: strategic)')
    parser.add_argument('--opponent-tightness', type=str, default='average',
                       choices=['very_tight', 'tight', 'average', 'loose', 'very_loose', 'any_two'],
                       help='Tightness level for strategic opponents (default: average)')
    
    args = parser.parse_args()
    
    run_interpretable_demo(
        num_games=args.num_games,
        tree_dir=args.tree_dir,
        show_explanations=not args.no_explanations,
        show_all_players=args.show_all,
        opponent_type=args.opponent_type,
        opponent_tightness=args.opponent_tightness
    )

if __name__ == "__main__":
    main()

