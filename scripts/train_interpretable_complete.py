#!/usr/bin/env python3
"""
Complete training pipeline for interpretable poker AI.
Runs the full pipeline from CFR training to decision tree training to evaluation.
"""

import os
import sys
import argparse
import time
from typing import Dict, Any

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.training.train_interpretable import train_interpretable_cfr
from src.interpretable.tree_trainer import train_interpretable_trees
from src.interpretable.visualizer import visualize_all_trees, create_strategy_chart
from scripts.evaluate_interpretable import InterpretableEvaluator
from src.interpretable.interpretable_agent import InterpretablePokerAgent

def main():
    """Main training pipeline function."""
    parser = argparse.ArgumentParser(description='Complete interpretable poker AI training pipeline')
    parser.add_argument('--iterations', type=int, default=1000, help='CFR iterations')
    parser.add_argument('--traversals', type=int, default=200, help='Traversals per iteration')
    parser.add_argument('--tree-depth', type=int, default=12, help='Maximum tree depth')
    parser.add_argument('--eval-games', type=int, default=500, help='Games for evaluation')
    parser.add_argument('--quick', action='store_true', help='Run quick training (fewer iterations)')
    parser.add_argument('--skip-cfr', action='store_true', help='Skip CFR training (use existing data)')
    parser.add_argument('--skip-trees', action='store_true', help='Skip tree training (use existing trees)')
    parser.add_argument('--skip-eval', action='store_true', help='Skip evaluation')
    parser.add_argument('--output-dir', type=str, default='interpretable_output', help='Output directory')
    
    args = parser.parse_args()
    
    if args.quick:
        args.iterations = 100
        args.traversals = 50
        args.eval_games = 100
    
    print("=" * 60)
    print("INTERPRETABLE POKER AI - COMPLETE TRAINING PIPELINE")
    print("=" * 60)
    print(f"CFR Iterations: {args.iterations}")
    print(f"Traversals per iteration: {args.traversals}")
    print(f"Tree depth: {args.tree_depth}")
    print(f"Evaluation games: {args.eval_games}")
    print(f"Output directory: {args.output_dir}")
    print("=" * 60)
    
    # Create output directories
    os.makedirs(args.output_dir, exist_ok=True)
    data_dir = os.path.join(args.output_dir, 'data')
    model_dir = os.path.join(args.output_dir, 'models')
    viz_dir = os.path.join(args.output_dir, 'visualizations')
    eval_dir = os.path.join(args.output_dir, 'evaluation')
    
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(viz_dir, exist_ok=True)
    os.makedirs(eval_dir, exist_ok=True)
    
    start_time = time.time()
    
    # Step 1: CFR Training with Data Collection
    if not args.skip_cfr:
        print("\n" + "=" * 40)
        print("STEP 1: CFR TRAINING WITH DATA COLLECTION")
        print("=" * 40)
        
        cfr_start = time.time()
        agent, data_collector = train_interpretable_cfr(
            num_iterations=args.iterations,
            traversals_per_iteration=args.traversals,
            save_dir=model_dir,
            log_dir=os.path.join(args.output_dir, 'logs'),
            data_dir=data_dir,
            verbose=True
        )
        cfr_time = time.time() - cfr_start
        
        print(f"CFR training completed in {cfr_time:.1f} seconds")
        
        # Print data collection statistics
        stats = data_collector.get_dataset_summary()
        print(f"Data collected: {stats['total_decisions']} decisions")
        print(f"By street: {stats['decisions_by_street']}")
        print(f"Actions: {stats['actions_taken']}")
    else:
        print("Skipping CFR training (using existing data)")
    
    # Step 2: Decision Tree Training
    if not args.skip_trees:
        print("\n" + "=" * 40)
        print("STEP 2: DECISION TREE TRAINING")
        print("=" * 40)
        
        tree_start = time.time()
        trainer = train_interpretable_trees(
            data_dir=data_dir,
            output_dir=model_dir,
            max_depth=args.tree_depth
        )
        tree_time = time.time() - tree_start
        
        print(f"Tree training completed in {tree_time:.1f} seconds")
        
        # Print tree statistics
        summary = trainer.get_tree_summary()
        print(f"Trees trained: {summary['n_trees']}")
        print(f"Streets: {summary['streets']}")
        
        for street in summary['streets']:
            if f'{street}_depth' in summary:
                print(f"  {street}: depth={summary[f'{street}_depth']}, leaves={summary[f'{street}_leaves']}")
    else:
        print("Skipping tree training (using existing trees)")
    
    # Step 3: Visualization
    print("\n" + "=" * 40)
    print("STEP 3: TREE VISUALIZATION")
    print("=" * 40)
    
    viz_start = time.time()
    
    # Load trees for visualization
    from src.interpretable.tree_trainer import InterpretableTreeTrainer
    trainer = InterpretableTreeTrainer()
    trees = trainer.load_trees(model_dir)
    
    if trees:
        # Create visualizations
        output_paths = visualize_all_trees(trees, viz_dir)
        print(f"Tree visualizations created: {len(output_paths)} files")
        
        # Create strategy chart
        strategy_path = create_strategy_chart(trees, os.path.join(viz_dir, 'strategy_chart.md'))
        if strategy_path:
            print(f"Strategy chart: {strategy_path}")
        
        viz_time = time.time() - viz_start
        print(f"Visualization completed in {viz_time:.1f} seconds")
    else:
        print("No trees found for visualization")
    
    # Step 4: Evaluation
    if not args.skip_eval:
        print("\n" + "=" * 40)
        print("STEP 4: PERFORMANCE EVALUATION")
        print("=" * 40)
        
        eval_start = time.time()
        
        # Create interpretable agent
        interpretable_agent = InterpretablePokerAgent(player_id=0, tree_dir=model_dir)
        
        # Create evaluator
        evaluator = InterpretableEvaluator(interpretable_agent)
        
        # Evaluate against random opponents
        print("Evaluating against random opponents...")
        random_results = evaluator.evaluate_against_random(args.eval_games)
        
        # Evaluate decision accuracy
        print("Evaluating decision accuracy...")
        accuracy_results = evaluator.evaluate_decision_accuracy(data_dir)
        
        # Save results
        evaluator.save_results(eval_dir)
        
        eval_time = time.time() - eval_start
        print(f"Evaluation completed in {eval_time:.1f} seconds")
        
        # Print summary
        print("\n" + "=" * 30)
        print("EVALUATION SUMMARY")
        print("=" * 30)
        
        if random_results:
            print(f"Average profit vs random: {random_results['avg_profit_per_game']:.2f}")
            print(f"Win rate: {random_results['win_rate']:.1%}")
            print(f"Action distribution: {random_results['action_distribution']}")
        
        if accuracy_results:
            print("Decision accuracy:")
            for street, results in accuracy_results.items():
                print(f"  {street}: {results['accuracy']:.3f}")
    else:
        print("Skipping evaluation")
    
    # Final summary
    total_time = time.time() - start_time
    print("\n" + "=" * 60)
    print("TRAINING PIPELINE COMPLETED")
    print("=" * 60)
    print(f"Total time: {total_time:.1f} seconds")
    print(f"Output directory: {args.output_dir}")
    print("\nGenerated files:")
    print(f"  - Data: {data_dir}")
    print(f"  - Models: {model_dir}")
    print(f"  - Visualizations: {viz_dir}")
    print(f"  - Evaluation: {eval_dir}")
    print("\nNext steps:")
    print("  1. Review visualizations in the visualizations/ directory")
    print("  2. Check evaluation results in the evaluation/ directory")
    print("  3. Use the Jupyter notebook for interactive analysis")
    print("  4. Play against the interpretable agent to test it")

if __name__ == "__main__":
    main()



