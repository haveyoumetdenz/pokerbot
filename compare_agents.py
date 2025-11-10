#!/usr/bin/env python3
"""
Compare DeepCFR agent vs Interpretable agent performance.
Runs both agents for the same number of games and shows side-by-side comparison.
"""

import os
import sys
import pokers as pkrs
import torch
import numpy as np
import random
import argparse
import glob
from src.core.deep_cfr import DeepCFRAgent
from src.interpretable.interpretable_agent import InterpretablePokerAgent
from src.agents.random_agent import RandomAgent
from src.agents.strategic_agent import StrategicAgent

def run_agent_games(agent, agent_type, num_games=50, device='cpu', verbose=False,
                    opponent_type='strategic', opponent_tightness='average'):
    """Run games with a specific agent and return statistics."""
    print(f"\n{'='*70}")
    print(f"🎮 Running {agent_type} agent for {num_games} games...")
    print(f"Opponent type: {opponent_type}")
    if opponent_type == 'strategic':
        print(f"Opponent tightness: {opponent_tightness}")
    print(f"{'='*70}")
    
    total_profit = 0
    wins = 0
    total_actions = 0
    action_counts = {'fold': 0, 'call': 0, 'raise': 0}
    
    for game_num in range(1, num_games + 1):
        # Create opponents based on type
        if opponent_type == 'strategic':
            if opponent_tightness == 'mixed':
                # Distribute different tightness levels across opponents
                tightness_levels = ['very_tight', 'tight', 'average', 'loose', 'very_loose']
                opponents = [StrategicAgent(i, tightness=tightness_levels[(i-1) % len(tightness_levels)]) for i in range(1, 6)]
            else:
                opponents = [StrategicAgent(i, tightness=opponent_tightness) for i in range(1, 6)]
        else:
            opponents = [RandomAgent(i) for i in range(1, 6)]
        agents = [agent] + opponents
        
        # Start new game for betting history tracking (if interpretable agent)
        if hasattr(agent, 'start_new_game'):
            agent.start_new_game()
        
        # Create a new game
        state = pkrs.State.from_seed(
            n_players=6,
            button=(game_num - 1) % 6,
            sb=1,
            bb=2,
            stake=200.0,
            seed=random.randint(0, 100000)
        )
        
        round_num = 0
        max_rounds = 100  # Safety limit
        
        while not state.final_state and round_num < max_rounds:
            current_player = state.current_player
            round_num += 1
            
            # Get action
            action = agents[current_player].choose_action(state)
            
            # Record action for betting history (for opponents only; interpretable agent records its own)
            if hasattr(agent, 'record_action') and current_player != 0:
                agent.record_action(state, current_player, action)
            
            # Track actions for the main agent
            if current_player == 0:
                total_actions += 1
                if action.action == pkrs.ActionEnum.Fold:
                    action_counts['fold'] += 1
                elif action.action in [pkrs.ActionEnum.Check, pkrs.ActionEnum.Call]:
                    action_counts['call'] += 1
                elif action.action == pkrs.ActionEnum.Raise:
                    action_counts['raise'] += 1
            
            # Apply action
            new_state = state.apply_action(action)
            
            if new_state.status != pkrs.StateStatus.Ok:
                if verbose:
                    print(f"⚠️  Invalid action in game {game_num}! Status: {new_state.status}")
                break
            
            state = new_state
        
        # Track performance
        if state.final_state:
            profit = state.players_state[0].reward
            total_profit += profit
            if profit > 0:
                wins += 1
        
        # Progress update every 10 games
        if game_num % 10 == 0:
            print(f"  Completed {game_num}/{num_games} games... (Wins: {wins}, Profit: ${total_profit:.2f})")
    
    # Calculate statistics
    win_rate = wins / num_games if num_games > 0 else 0
    avg_profit = total_profit / num_games if num_games > 0 else 0
    
    return {
        'total_profit': total_profit,
        'avg_profit': avg_profit,
        'wins': wins,
        'win_rate': win_rate,
        'total_games': num_games,
        'total_actions': total_actions,
        'action_distribution': action_counts
    }

def compare_agents(num_games=50, deepcfr_dir='models', interpretable_dir='interpretable_output/models/models', 
                  device='cpu', verbose=False, opponent_type='strategic', opponent_tightness='average'):
    """Compare DeepCFR and Interpretable agents."""
    
    print("\n" + "="*70)
    print("🤖 AGENT COMPARISON: DeepCFR vs Interpretable")
    print("="*70)
    print(f"Games per agent: {num_games}")
    print(f"DeepCFR models: {deepcfr_dir}")
    print(f"Interpretable trees: {interpretable_dir}")
    print(f"Opponent type: {opponent_type}")
    if opponent_type == 'strategic':
        print(f"Opponent tightness: {opponent_tightness}")
    print()
    
    # Load DeepCFR agent
    deepcfr_agent = None
    deepcfr_stats = None
    
    if os.path.isdir(deepcfr_dir):
        try:
            # Find latest checkpoint
            checkpoints = sorted(glob.glob(os.path.join(deepcfr_dir, "*.pt")))
            if checkpoints:
                deepcfr_agent = DeepCFRAgent(player_id=0, num_players=6, device=device)
                deepcfr_agent.load_model(checkpoints[-1])
                print(f"✅ Loaded DeepCFR agent from: {os.path.basename(checkpoints[-1])}")
                
                # Run DeepCFR games
                deepcfr_stats = run_agent_games(deepcfr_agent, "DeepCFR", num_games, device, verbose,
                                              opponent_type, opponent_tightness)
            else:
                print(f"⚠️  No DeepCFR models found in {deepcfr_dir}")
        except Exception as e:
            print(f"❌ Error loading DeepCFR agent: {e}")
    else:
        print(f"⚠️  DeepCFR directory not found: {deepcfr_dir}")
    
    # Load Interpretable agent
    interpretable_agent = None
    interpretable_stats = None
    
    if os.path.isdir(interpretable_dir):
        try:
            interpretable_agent = InterpretablePokerAgent(player_id=0, tree_dir=interpretable_dir)
            print(f"✅ Loaded Interpretable agent from: {interpretable_dir}")
            
            # Run Interpretable games
            interpretable_stats = run_agent_games(interpretable_agent, "Interpretable", num_games, device, verbose,
                                                 opponent_type, opponent_tightness)
        except Exception as e:
            print(f"❌ Error loading Interpretable agent: {e}")
    else:
        print(f"⚠️  Interpretable directory not found: {interpretable_dir}")
    
    # Show comparison results
    print(f"\n{'='*70}")
    print("📊 COMPARISON RESULTS")
    print(f"{'='*70}\n")
    
    if deepcfr_stats and interpretable_stats:
        # Side-by-side comparison
        print(f"{'Metric':<30} {'DeepCFR':<20} {'Interpretable':<20} {'Difference':<15}")
        print("-" * 85)
        
        # Win rate
        wr_diff = deepcfr_stats['win_rate'] - interpretable_stats['win_rate']
        print(f"{'Win Rate':<30} {deepcfr_stats['win_rate']:<20.1%} {interpretable_stats['win_rate']:<20.1%} {wr_diff:+.1%}")
        
        # Total profit
        profit_diff = deepcfr_stats['total_profit'] - interpretable_stats['total_profit']
        print(f"{'Total Profit':<30} ${deepcfr_stats['total_profit']:<19.2f} ${interpretable_stats['total_profit']:<19.2f} ${profit_diff:+.2f}")
        
        # Average profit per game
        avg_diff = deepcfr_stats['avg_profit'] - interpretable_stats['avg_profit']
        print(f"{'Avg Profit/Game':<30} ${deepcfr_stats['avg_profit']:<19.2f} ${interpretable_stats['avg_profit']:<19.2f} ${avg_diff:+.2f}")
        
        # Wins
        wins_diff = deepcfr_stats['wins'] - interpretable_stats['wins']
        print(f"{'Wins':<30} {deepcfr_stats['wins']:<20} {interpretable_stats['wins']:<20} {wins_diff:+d}")
        
        # Action distribution
        print(f"\n{'Action Distribution:'}")
        print(f"  {'Folds':<28} {deepcfr_stats['action_distribution']['fold']:<20} {interpretable_stats['action_distribution']['fold']:<20}")
        print(f"  {'Calls':<28} {deepcfr_stats['action_distribution']['call']:<20} {interpretable_stats['action_distribution']['call']:<20}")
        print(f"  {'Raises':<28} {deepcfr_stats['action_distribution']['raise']:<20} {interpretable_stats['action_distribution']['raise']:<20}")
        
        # Summary
        print(f"\n{'='*70}")
        print("📈 SUMMARY")
        print(f"{'='*70}")
        
        if deepcfr_stats['avg_profit'] > interpretable_stats['avg_profit']:
            diff_pct = ((deepcfr_stats['avg_profit'] - interpretable_stats['avg_profit']) / abs(interpretable_stats['avg_profit']) * 100) if interpretable_stats['avg_profit'] != 0 else 0
            print(f"🏆 DeepCFR performs {'better' if diff_pct > 0 else 'worse'}: ${deepcfr_stats['avg_profit'] - interpretable_stats['avg_profit']:.2f} more per game ({diff_pct:.1f}% difference)")
        else:
            diff_pct = ((interpretable_stats['avg_profit'] - deepcfr_stats['avg_profit']) / abs(deepcfr_stats['avg_profit']) * 100) if deepcfr_stats['avg_profit'] != 0 else 0
            print(f"🏆 Interpretable performs {'better' if diff_pct > 0 else 'worse'}: ${interpretable_stats['avg_profit'] - deepcfr_stats['avg_profit']:.2f} more per game ({diff_pct:.1f}% difference)")
        
        # Win rate comparison
        if deepcfr_stats['win_rate'] > interpretable_stats['win_rate']:
            print(f"✅ DeepCFR has higher win rate: {deepcfr_stats['win_rate']:.1%} vs {interpretable_stats['win_rate']:.1%}")
        else:
            print(f"✅ Interpretable has higher win rate: {interpretable_stats['win_rate']:.1%} vs {deepcfr_stats['win_rate']:.1%}")
    
    elif deepcfr_stats:
        print("📊 DeepCFR Agent Results:")
        print(f"  Win Rate: {deepcfr_stats['win_rate']:.1%}")
        print(f"  Total Profit: ${deepcfr_stats['total_profit']:.2f}")
        print(f"  Avg Profit/Game: ${deepcfr_stats['avg_profit']:.2f}")
        print(f"  Wins: {deepcfr_stats['wins']}/{deepcfr_stats['total_games']}")
        print("\n⚠️  Interpretable agent not available for comparison")
    
    elif interpretable_stats:
        print("📊 Interpretable Agent Results:")
        print(f"  Win Rate: {interpretable_stats['win_rate']:.1%}")
        print(f"  Total Profit: ${interpretable_stats['total_profit']:.2f}")
        print(f"  Avg Profit/Game: ${interpretable_stats['avg_profit']:.2f}")
        print(f"  Wins: {interpretable_stats['wins']}/{interpretable_stats['total_games']}")
        print("\n⚠️  DeepCFR agent not available for comparison")
    else:
        print("❌ No agents available to compare!")
    
    print(f"\n{'='*70}")

def main():
    parser = argparse.ArgumentParser(description='Compare DeepCFR vs Interpretable agent performance')
    parser.add_argument('--num-games', type=int, default=50,
                       help='Number of games to run per agent (default: 50)')
    parser.add_argument('--deepcfr-dir', type=str, default='models',
                       help='Directory containing DeepCFR models (.pt files)')
    parser.add_argument('--interpretable-dir', type=str, default='interpretable_output/models/models',
                       help='Directory containing interpretable trees (.pkl files)')
    parser.add_argument('--verbose', action='store_true',
                       help='Show verbose output during games')
    parser.add_argument('--opponent-type', type=str, default='strategic',
                       choices=['random', 'strategic'],
                       help='Type of opponent: random or strategic (default: strategic)')
    parser.add_argument('--opponent-tightness', type=str, default='average',
                       choices=['very_tight', 'tight', 'average', 'loose', 'very_loose', 'any_two', 'mixed'],
                       help='Tightness level for strategic opponents (default: average). Use "mixed" for variety across opponents.')
    
    args = parser.parse_args()
    
    # Device configuration
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    compare_agents(
        num_games=args.num_games,
        deepcfr_dir=args.deepcfr_dir,
        interpretable_dir=args.interpretable_dir,
        device=device,
        verbose=args.verbose,
        opponent_type=args.opponent_type,
        opponent_tightness=args.opponent_tightness
    )

if __name__ == "__main__":
    main()

