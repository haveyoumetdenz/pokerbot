#!/usr/bin/env python3
"""
Diagnostic script for interpretable agent performance.
Provides detailed analysis of interpretable agent vs DeepCFR.
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

def run_diagnostic(agent, agent_type, num_games=50, opponent_type='strategic', 
                   opponent_tightness='mixed', verbose=False):
    """Run detailed diagnostic on agent performance."""
    
    print(f"\n{'='*70}")
    print(f"🔍 DIAGNOSTIC: {agent_type} Agent")
    print(f"{'='*70}")
    print(f"Games: {num_games}")
    print(f"Opponents: {opponent_type} ({opponent_tightness})")
    print(f"{'='*70}\n")
    
    total_profit = 0
    wins = 0
    total_actions = 0
    action_counts = {'fold': 0, 'call': 0, 'raise': 0}
    
    # Track by street
    street_profits = {'preflop': [], 'flop': [], 'turn': [], 'river': []}
    street_actions = {'preflop': {'fold': 0, 'call': 0, 'raise': 0},
                     'flop': {'fold': 0, 'call': 0, 'raise': 0},
                     'turn': {'fold': 0, 'call': 0, 'raise': 0},
                     'river': {'fold': 0, 'call': 0, 'raise': 0}}
    
    # Track decision quality
    high_equity_folds = 0
    high_equity_raises = 0
    low_equity_calls = 0
    
    # Betting history tracking (for interpretable agent)
    betting_history_available = False
    if hasattr(agent, 'betting_history'):
        betting_history_available = True
        agent.start_new_game()
    
    for game_num in range(1, num_games + 1):
        # Create opponents
        if opponent_type == 'strategic':
            if opponent_tightness == 'mixed':
                tightness_levels = ['very_tight', 'tight', 'average', 'loose', 'very_loose']
                opponents = [StrategicAgent(i, tightness=tightness_levels[(i-1) % len(tightness_levels)]) 
                            for i in range(1, 6)]
            else:
                opponents = [StrategicAgent(i, tightness=opponent_tightness) for i in range(1, 6)]
        else:
            opponents = [RandomAgent(i) for i in range(1, 6)]
        agents = [agent] + opponents
        
        # Start new game for betting history
        if hasattr(agent, 'start_new_game'):
            agent.start_new_game()
        
        # Create game
        state = pkrs.State.from_seed(
            n_players=6,
            button=(game_num - 1) % 6,
            sb=1,
            bb=2,
            stake=200.0,
            seed=random.randint(0, 100000)
        )
        
        round_num = 0
        max_rounds = 100
        current_street = 'preflop'
        
        while not state.final_state and round_num < max_rounds:
            current_player = state.current_player
            round_num += 1
            
            # Track street
            street_names = ['preflop', 'flop', 'turn', 'river', 'showdown']
            if int(state.stage) < len(street_names):
                current_street = street_names[int(state.stage)]
            
            # Get action
            action = agents[current_player].choose_action(state)
            
            # Record opponent actions for betting history (before applying action)
            if hasattr(agent, 'record_action') and current_player != 0:
                try:
                    # Get street name for recording
                    street_names = ['preflop', 'flop', 'turn', 'river', 'showdown']
                    street = street_names[int(state.stage)] if int(state.stage) < len(street_names) else 'unknown'
                    agent.record_action(state, current_player, action)
                except Exception as e:
                    if verbose:
                        print(f"Warning: Failed to record action for player {current_player}: {e}")
            
            # Track main agent actions
            if current_player == 0:
                total_actions += 1
                
                # Track actions by street
                if action.action == pkrs.ActionEnum.Fold:
                    action_counts['fold'] += 1
                    street_actions[current_street]['fold'] += 1
                elif action.action in [pkrs.ActionEnum.Check, pkrs.ActionEnum.Call]:
                    action_counts['call'] += 1
                    street_actions[current_street]['call'] += 1
                elif action.action == pkrs.ActionEnum.Raise:
                    action_counts['raise'] += 1
                    street_actions[current_street]['raise'] += 1
                
                # Analyze decision quality (if interpretable agent)
                if agent_type == 'Interpretable':
                    try:
                        explanation = agent.explain_decision(state)
                        features = explanation.get('features', {})
                        hand_equity = features.get('hand_equity', 0)
                        
                        if action.action == pkrs.ActionEnum.Fold and hand_equity > 0.6:
                            high_equity_folds += 1
                        elif action.action == pkrs.ActionEnum.Raise and hand_equity > 0.6:
                            high_equity_raises += 1
                        elif action.action in [pkrs.ActionEnum.Call, pkrs.ActionEnum.Check] and hand_equity < 0.3:
                            low_equity_calls += 1
                    except:
                        pass
            
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
    
    # Calculate statistics
    win_rate = wins / num_games if num_games > 0 else 0
    avg_profit = total_profit / num_games if num_games > 0 else 0
    
    # Action distribution percentages
    if total_actions > 0:
        action_dist_pct = {
            'fold': action_counts['fold'] / total_actions * 100,
            'call': action_counts['call'] / total_actions * 100,
            'raise': action_counts['raise'] / total_actions * 100
        }
    else:
        action_dist_pct = {'fold': 0, 'call': 0, 'raise': 0}
    
    # Betting history stats (if available)
    betting_stats = {}
    if betting_history_available and hasattr(agent, 'betting_history'):
        bh = agent.betting_history
        betting_stats = {
            'games_played': bh.get('game_count', 0),
            'opponents_tracked': len(bh.get('opponent_stats', {})),
            'street_stats': bh.get('street_stats', {})
        }
    
    return {
        'agent_type': agent_type,
        'total_profit': total_profit,
        'avg_profit': avg_profit,
        'wins': wins,
        'win_rate': win_rate,
        'total_actions': total_actions,
        'action_counts': action_counts,
        'action_distribution_pct': action_dist_pct,
        'street_actions': street_actions,
        'high_equity_folds': high_equity_folds,
        'high_equity_raises': high_equity_raises,
        'low_equity_calls': low_equity_calls,
        'betting_history_available': betting_history_available,
        'betting_stats': betting_stats
    }

def print_diagnostic_report(deepcfr_stats, interpretable_stats):
    """Print detailed diagnostic report."""
    
    print(f"\n{'='*70}")
    print("📊 DETAILED DIAGNOSTIC REPORT")
    print(f"{'='*70}\n")
    
    # Overall Performance
    print("📈 OVERALL PERFORMANCE")
    print("-" * 70)
    print(f"{'Metric':<30} {'DeepCFR':<20} {'Interpretable':<20}")
    print("-" * 70)
    print(f"{'Win Rate':<30} {deepcfr_stats['win_rate']:.1%}{'':<13} {interpretable_stats['win_rate']:.1%}")
    print(f"{'Total Profit':<30} ${deepcfr_stats['total_profit']:.2f}{'':<12} ${interpretable_stats['total_profit']:.2f}")
    print(f"{'Avg Profit/Game':<30} ${deepcfr_stats['avg_profit']:.2f}{'':<12} ${interpretable_stats['avg_profit']:.2f}")
    print(f"{'Wins':<30} {deepcfr_stats['wins']}{'':<15} {interpretable_stats['wins']}")
    print(f"{'Total Actions':<30} {deepcfr_stats['total_actions']}{'':<15} {interpretable_stats['total_actions']}")
    
    diff_profit = deepcfr_stats['avg_profit'] - interpretable_stats['avg_profit']
    diff_winrate = deepcfr_stats['win_rate'] - interpretable_stats['win_rate']
    print(f"\n{'Difference':<30} {diff_profit:+.2f} per game ({diff_profit/interpretable_stats['avg_profit']*100 if interpretable_stats['avg_profit'] > 0 else 0:+.1f}%)")
    print(f"{'Win Rate Delta':<30} {diff_winrate:+.1%}")
    
    # Action Distribution
    print(f"\n🎯 ACTION DISTRIBUTION")
    print("-" * 70)
    print(f"{'Action':<30} {'DeepCFR':<20} {'Interpretable':<20}")
    print("-" * 70)
    for action in ['fold', 'call', 'raise']:
        dcfr_pct = deepcfr_stats['action_distribution_pct'][action]
        inter_pct = interpretable_stats['action_distribution_pct'][action]
        print(f"{action.upper():<30} {dcfr_pct:.1f}%{'':<13} {inter_pct:.1f}%")
    
    # Street Analysis
    print(f"\n📊 PERFORMANCE BY STREET (Interpretable Agent)")
    print("-" * 70)
    print(f"{'Street':<20} {'Folds':<15} {'Calls':<15} {'Raises':<15}")
    print("-" * 70)
    for street in ['preflop', 'flop', 'turn', 'river']:
        actions = interpretable_stats['street_actions'][street]
        total = sum(actions.values())
        if total > 0:
            print(f"{street:<20} {actions['fold']:>3} ({actions['fold']/total*100:>5.1f}%) {'':<3} "
                  f"{actions['call']:>3} ({actions['call']/total*100:>5.1f}%) {'':<3} "
                  f"{actions['raise']:>3} ({actions['raise']/total*100:>5.1f}%)")
        else:
            print(f"{street:<20} {'N/A':<15} {'N/A':<15} {'N/A':<15}")
    
    # Decision Quality Analysis
    if interpretable_stats['total_actions'] > 0:
        print(f"\n🎲 DECISION QUALITY (Interpretable Agent)")
        print("-" * 70)
        print(f"High Equity Folds (>60% equity): {interpretable_stats['high_equity_folds']}")
        print(f"High Equity Raises (>60% equity): {interpretable_stats['high_equity_raises']}")
        print(f"Low Equity Calls (<30% equity): {interpretable_stats['low_equity_calls']}")
        
        if interpretable_stats['high_equity_folds'] > 0:
            print(f"⚠️  WARNING: {interpretable_stats['high_equity_folds']} high-equity folds detected!")
    
    # Betting History Status
    if interpretable_stats['betting_history_available']:
        print(f"\n📚 BETTING HISTORY STATUS")
        print("-" * 70)
        bh_stats = interpretable_stats['betting_stats']
        print(f"Games Played: {bh_stats.get('games_played', 0)}")
        print(f"Opponents Tracked: {bh_stats.get('opponents_tracked', 0)}")
        
        street_stats = bh_stats.get('street_stats', {})
        if street_stats:
            print(f"\nStreet-Level Statistics:")
            for street, stats in street_stats.items():
                total = stats.get('total', 0)
                if total > 0:
                    print(f"  {street}: {total} total actions")
                    print(f"    Raises: {stats.get('raises', 0)} ({stats.get('raises', 0)/total*100:.1f}%)")
                    print(f"    Calls: {stats.get('calls', 0)} ({stats.get('calls', 0)/total*100:.1f}%)")
                    print(f"    Folds: {stats.get('folds', 0)} ({stats.get('folds', 0)/total*100:.1f}%)")
    else:
        print(f"\n📚 BETTING HISTORY: Not available")
    
    # Summary
    print(f"\n{'='*70}")
    print("💡 SUMMARY & RECOMMENDATIONS")
    print(f"{'='*70}")
    
    if interpretable_stats['avg_profit'] >= deepcfr_stats['avg_profit'] * 0.9:
        print("✅ Interpretable agent performing well (within 10% of DeepCFR)")
    elif interpretable_stats['avg_profit'] >= deepcfr_stats['avg_profit'] * 0.8:
        print("⚠️  Interpretable agent performing acceptably (within 20% of DeepCFR)")
    else:
        print("❌ Interpretable agent underperforming (>20% below DeepCFR)")
    
    if interpretable_stats['high_equity_folds'] > interpretable_stats['total_actions'] * 0.05:
        print("⚠️  WARNING: High number of high-equity folds detected - trees may be too conservative")
    
    if not interpretable_stats['betting_history_available']:
        print("ℹ️  Betting history features are implemented but trees weren't trained with them")
        print("   Recommendation: Retrain trees with betting history features for better performance")

def main():
    parser = argparse.ArgumentParser(description='Diagnostic comparison of DeepCFR vs Interpretable agent')
    parser.add_argument('--num-games', type=int, default=50,
                       help='Number of games to run per agent (default: 50)')
    parser.add_argument('--deepcfr-dir', type=str, default='models',
                       help='Directory containing DeepCFR models (.pt files)')
    parser.add_argument('--interpretable-dir', type=str, default='interpretable_output/models/models',
                       help='Directory containing interpretable trees (.pkl files)')
    parser.add_argument('--opponent-type', type=str, default='strategic',
                       choices=['random', 'strategic'],
                       help='Type of opponent (default: strategic)')
    parser.add_argument('--opponent-tightness', type=str, default='mixed',
                       choices=['very_tight', 'tight', 'average', 'loose', 'very_loose', 'any_two', 'mixed'],
                       help='Tightness level for strategic opponents (default: mixed)')
    parser.add_argument('--verbose', action='store_true',
                       help='Show verbose output')
    
    args = parser.parse_args()
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    # Load DeepCFR agent
    deepcfr_agent = None
    if os.path.isdir(args.deepcfr_dir):
        checkpoints = sorted(glob.glob(os.path.join(args.deepcfr_dir, "*.pt")))
        if checkpoints:
            deepcfr_agent = DeepCFRAgent(player_id=0, num_players=6, device=device)
            deepcfr_agent.load_model(checkpoints[-1])
            print(f"✅ Loaded DeepCFR: {os.path.basename(checkpoints[-1])}")
    
    # Load Interpretable agent
    interpretable_agent = None
    if os.path.isdir(args.interpretable_dir):
        interpretable_agent = InterpretablePokerAgent(player_id=0, tree_dir=args.interpretable_dir)
        print(f"✅ Loaded Interpretable agent")
    
    if not deepcfr_agent or not interpretable_agent:
        print("❌ Error: Could not load both agents")
        return
    
    # Run diagnostics
    deepcfr_stats = run_diagnostic(
        deepcfr_agent, "DeepCFR", args.num_games, 
        args.opponent_type, args.opponent_tightness, args.verbose
    )
    
    interpretable_stats = run_diagnostic(
        interpretable_agent, "Interpretable", args.num_games,
        args.opponent_type, args.opponent_tightness, args.verbose
    )
    
    # Print report
    print_diagnostic_report(deepcfr_stats, interpretable_stats)

if __name__ == "__main__":
    main()

