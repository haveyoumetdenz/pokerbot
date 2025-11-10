#!/usr/bin/env python3
"""
Evaluation script for interpretable poker AI.
Compares interpretable agent vs neural network performance.
"""

import os
import sys
import argparse
import time
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
import pokers as pkrs

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.interpretable.interpretable_agent import InterpretablePokerAgent
from src.core.deep_cfr import DeepCFRAgent
from src.agents.random_agent import RandomAgent

class InterpretableEvaluator:
    """Evaluates interpretable poker AI against various opponents."""
    
    def __init__(self, interpretable_agent: InterpretablePokerAgent, 
                 neural_agent: DeepCFRAgent = None):
        self.interpretable_agent = interpretable_agent
        self.neural_agent = neural_agent
        self.evaluation_results = {}
    
    def evaluate_against_random(self, num_games: int = 1000) -> Dict[str, Any]:
        """Evaluate interpretable agent against random opponents."""
        print(f"Evaluating interpretable agent against random opponents ({num_games} games)...")
        
        total_profit = 0
        completed_games = 0
        decision_times = []
        action_distribution = {'fold': 0, 'call': 0, 'raise': 0}
        wins = 0
        
        for game in range(num_games):
            try:
                # Create game state
                state = pkrs.State.from_seed(
                    n_players=6,
                    button=game % 6,
                    sb=1,
                    bb=2,
                    stake=200.0,
                    seed=game
                )
                
                # Create random opponents
                random_agents = [RandomAgent(i) for i in range(6) if i != 0]
                random_agents.insert(0, None)  # Insert None for the trained agent
                
                # Play game
                start_time = time.time()
                while not state.final_state:
                    current_player = state.current_player
                    
                    if current_player == 0:  # Interpretable agent
                        action = self.interpretable_agent.choose_action(state)
                        decision_time = time.time() - start_time
                        decision_times.append(decision_time)
                        
                        # Record action for analysis
                        if hasattr(action, 'action'):
                            if action.action == pkrs.ActionEnum.Fold:
                                action_distribution['fold'] += 1
                            elif action.action in [pkrs.ActionEnum.Check, pkrs.ActionEnum.Call]:
                                action_distribution['call'] += 1
                            elif action.action == pkrs.ActionEnum.Raise:
                                action_distribution['raise'] += 1
                    else:
                        action = random_agents[current_player].choose_action(state)
                    
                    state = state.apply_action(action)
                
                # Record profit
                if state.final_state:
                    profit = state.players_state[0].reward
                    total_profit += profit
                    completed_games += 1
                    if profit > 0:
                        wins += 1
                
                if game % 100 == 0 and game > 0:
                    print(f"  Game {game}: Profit so far: {total_profit:.2f}")
                    
            except Exception as e:
                print(f"Error in game {game}: {e}")
                continue
        
        avg_profit = total_profit / completed_games if completed_games > 0 else 0
        avg_decision_time = np.mean(decision_times) if decision_times else 0
        
        results = {
            'total_profit': total_profit,
            'avg_profit_per_game': avg_profit,
            'completed_games': completed_games,
            'avg_decision_time': avg_decision_time,
            'action_distribution': action_distribution,
            'win_rate': (wins / completed_games) if completed_games > 0 else 0
        }
        
        self.evaluation_results['vs_random'] = results
        return results
    
    def evaluate_against_neural(self, num_games: int = 500) -> Dict[str, Any]:
        """Evaluate interpretable agent against neural network agent."""
        if self.neural_agent is None:
            print("No neural agent provided for comparison")
            return {}
        
        print(f"Evaluating interpretable vs neural agent ({num_games} games)...")
        
        interpretable_profit = 0
        neural_profit = 0
        completed_games = 0
        
        for game in range(num_games):
            try:
                # Create game state
                state = pkrs.State.from_seed(
                    n_players=6,
                    button=game % 6,
                    sb=1,
                    bb=2,
                    stake=200.0,
                    seed=game
                )
                
                # Create agents
                agents = [None] * 6
                agents[0] = self.interpretable_agent  # Interpretable agent
                agents[1] = self.neural_agent         # Neural agent
                # Fill remaining with random agents
                for i in range(2, 6):
                    agents[i] = RandomAgent(i)
                
                # Play game
                while not state.final_state:
                    current_player = state.current_player
                    action = agents[current_player].choose_action(state)
                    state = state.apply_action(action)
                
                # Record profits
                if state.final_state:
                    interpretable_profit += state.players_state[0].reward
                    neural_profit += state.players_state[1].reward
                    completed_games += 1
                
                if game % 50 == 0 and game > 0:
                    print(f"  Game {game}: Interpretable: {interpretable_profit:.2f}, Neural: {neural_profit:.2f}")
                    
            except Exception as e:
                print(f"Error in game {game}: {e}")
                continue
        
        results = {
            'interpretable_profit': interpretable_profit,
            'neural_profit': neural_profit,
            'profit_difference': interpretable_profit - neural_profit,
            'completed_games': completed_games,
            'interpretable_avg': interpretable_profit / completed_games if completed_games > 0 else 0,
            'neural_avg': neural_profit / completed_games if completed_games > 0 else 0
        }
        
        self.evaluation_results['vs_neural'] = results
        return results
    
    def evaluate_decision_accuracy(self, data_dir: str = 'data/interpretable') -> Dict[str, Any]:
        """Evaluate decision accuracy against ground truth CFR data."""
        print("Evaluating decision accuracy against CFR ground truth...")
        
        accuracy_results = {}
        
        for street in ['preflop', 'flop', 'turn', 'river']:
            data_file = os.path.join(data_dir, f'{street}_decisions.csv')
            if not os.path.exists(data_file):
                continue
            
            try:
                # Load data
                data = pd.read_csv(data_file)
                if data.empty:
                    continue
                
                correct_predictions = 0
                total_predictions = 0
                
                # Sample some decisions for testing
                sample_size = min(100, len(data))
                sample_data = data.sample(n=sample_size, random_state=42)
                
                for _, row in sample_data.iterrows():
                    try:
                        # Create mock state (simplified)
                        # In practice, you'd reconstruct the full state
                        state = pkrs.State.from_seed(
                            n_players=6,
                            button=0,
                            sb=1,
                            bb=2,
                            stake=200.0,
                            seed=int(row.get('iteration', 0))
                        )
                        
                        # Get interpretable agent decision
                        interpretable_action = self.interpretable_agent.choose_action(state)
                        
                        # Convert to category
                        if interpretable_action.action == pkrs.ActionEnum.Fold:
                            predicted_action = 'fold'
                        elif interpretable_action.action in [pkrs.ActionEnum.Check, pkrs.ActionEnum.Call]:
                            predicted_action = 'call'
                        elif interpretable_action.action == pkrs.ActionEnum.Raise:
                            predicted_action = 'raise'
                        else:
                            predicted_action = 'fold'
                        
                        # Compare with ground truth
                        true_action = row['action']
                        if predicted_action == true_action:
                            correct_predictions += 1
                        total_predictions += 1
                        
                    except Exception as e:
                        continue
                
                accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
                accuracy_results[street] = {
                    'accuracy': accuracy,
                    'correct': correct_predictions,
                    'total': total_predictions
                }
                
                print(f"  {street}: {accuracy:.3f} accuracy ({correct_predictions}/{total_predictions})")
                
            except Exception as e:
                print(f"Error evaluating {street}: {e}")
                continue
        
        self.evaluation_results['decision_accuracy'] = accuracy_results
        return accuracy_results
    
    def generate_performance_report(self) -> str:
        """Generate comprehensive performance report."""
        report = []
        report.append("# Interpretable Poker AI Performance Report")
        report.append("=" * 50)
        report.append("")
        
        # Random opponent results
        if 'vs_random' in self.evaluation_results:
            results = self.evaluation_results['vs_random']
            report.append("## Performance vs Random Opponents")
            report.append(f"- Average profit per game: {results['avg_profit_per_game']:.2f}")
            report.append(f"- Total profit: {results['total_profit']:.2f}")
            report.append(f"- Win rate: {results['win_rate']:.1%}")
            report.append(f"- Average decision time: {results['avg_decision_time']:.4f}s")
            report.append(f"- Action distribution: {results['action_distribution']}")
            report.append("")
        
        # Neural network comparison
        if 'vs_neural' in self.evaluation_results:
            results = self.evaluation_results['vs_neural']
            report.append("## Performance vs Neural Network")
            report.append(f"- Interpretable agent profit: {results['interpretable_profit']:.2f}")
            report.append(f"- Neural network profit: {results['neural_profit']:.2f}")
            report.append(f"- Profit difference: {results['profit_difference']:.2f}")
            report.append(f"- Performance ratio: {results['interpretable_avg'] / results['neural_avg']:.3f}" if results['neural_avg'] != 0 else "- Performance ratio: N/A")
            report.append("")
        
        # Decision accuracy
        if 'decision_accuracy' in self.evaluation_results:
            report.append("## Decision Accuracy vs CFR Ground Truth")
            for street, results in self.evaluation_results['decision_accuracy'].items():
                report.append(f"- {street}: {results['accuracy']:.3f} ({results['correct']}/{results['total']})")
            report.append("")
        
        # Interpretability metrics
        report.append("## Interpretability Metrics")
        strategy_summary = self.interpretable_agent.get_strategy_summary()
        if 'total_decisions' in strategy_summary:
            report.append(f"- Total decisions analyzed: {strategy_summary['total_decisions']}")
            report.append(f"- Action distribution: {strategy_summary['action_distribution']}")
            report.append(f"- Average hand equity: {strategy_summary['avg_hand_equity']:.3f}")
            report.append(f"- Average pot odds: {strategy_summary['avg_pot_odds']:.3f}")
        report.append("")
        
        # Tree complexity
        report.append("## Tree Complexity")
        for street, tree in self.interpretable_agent.trees.items():
            if tree is not None:
                report.append(f"- {street}: depth={tree.get_depth()}, leaves={tree.get_n_leaves()}")
        report.append("")
        
        return "\n".join(report)
    
    def save_results(self, output_dir: str = 'evaluation_results'):
        """Save evaluation results to files."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save results as JSON
        import json
        results_file = os.path.join(output_dir, 'evaluation_results.json')
        with open(results_file, 'w') as f:
            json.dump(self.evaluation_results, f, indent=2)
        
        # Save performance report
        report = self.generate_performance_report()
        report_file = os.path.join(output_dir, 'performance_report.md')
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"Results saved to {output_dir}")
        print(f"- Results: {results_file}")
        print(f"- Report: {report_file}")

def main():
    """Main evaluation function."""
    parser = argparse.ArgumentParser(description='Evaluate interpretable poker AI')
    parser.add_argument('--tree-dir', type=str, default='models/interpretable',
                       help='Directory containing trained trees')
    parser.add_argument('--neural-model', type=str, default=None,
                       help='Path to neural network model for comparison')
    parser.add_argument('--data-dir', type=str, default='data/interpretable',
                       help='Directory containing training data')
    parser.add_argument('--output-dir', type=str, default='evaluation_results',
                       help='Directory to save evaluation results')
    parser.add_argument('--num-games', type=int, default=1000,
                       help='Number of games to play for evaluation')
    parser.add_argument('--quick', action='store_true',
                       help='Run quick evaluation with fewer games')
    
    args = parser.parse_args()
    
    if args.quick:
        args.num_games = 100
    
    print("Starting interpretable poker AI evaluation...")
    print(f"Tree directory: {args.tree_dir}")
    print(f"Number of games: {args.num_games}")
    
    # Create interpretable agent
    interpretable_agent = InterpretablePokerAgent(player_id=0, tree_dir=args.tree_dir)
    
    # Create neural agent if provided
    neural_agent = None
    if args.neural_model and os.path.exists(args.neural_model):
        try:
            neural_agent = DeepCFRAgent(player_id=1, device='cpu')
            neural_agent.load_model(args.neural_model)
            print(f"Loaded neural agent from {args.neural_model}")
        except Exception as e:
            print(f"Error loading neural agent: {e}")
    
    # Create evaluator
    evaluator = InterpretableEvaluator(interpretable_agent, neural_agent)
    
    # Run evaluations
    print("\n1. Evaluating against random opponents...")
    evaluator.evaluate_against_random(args.num_games)
    
    if neural_agent:
        print("\n2. Evaluating against neural network...")
        evaluator.evaluate_against_neural(args.num_games // 2)
    
    print("\n3. Evaluating decision accuracy...")
    evaluator.evaluate_decision_accuracy(args.data_dir)
    
    # Generate and save results
    print("\n4. Generating performance report...")
    evaluator.save_results(args.output_dir)
    
    # Print summary
    print("\n" + "="*50)
    print("EVALUATION SUMMARY")
    print("="*50)
    
    if 'vs_random' in evaluator.evaluation_results:
        results = evaluator.evaluation_results['vs_random']
        print(f"Average profit vs random: {results['avg_profit_per_game']:.2f}")
        print(f"Win rate: {results['win_rate']:.1%}")
    
    if 'vs_neural' in evaluator.evaluation_results:
        results = evaluator.evaluation_results['vs_neural']
        print(f"Profit vs neural: {results['interpretable_profit']:.2f} vs {results['neural_profit']:.2f}")
        print(f"Performance ratio: {results['interpretable_avg'] / results['neural_avg']:.3f}" if results['neural_avg'] != 0 else "Performance ratio: N/A")
    
    if 'decision_accuracy' in evaluator.evaluation_results:
        print("Decision accuracy:")
        for street, results in evaluator.evaluation_results['decision_accuracy'].items():
            print(f"  {street}: {results['accuracy']:.3f}")
    
    print(f"\nDetailed results saved to {args.output_dir}")

if __name__ == "__main__":
    main()



