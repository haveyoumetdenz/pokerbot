#!/usr/bin/env python3
"""
Command-line tool to generate all visualizations for interpretable poker trees.
"""

import os
import sys
import argparse

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.interpretable.visualizer import visualize_all_trees, create_strategy_chart
from src.interpretable.tree_trainer import InterpretableTreeTrainer

def main():
    """Main function for tree visualization."""
    parser = argparse.ArgumentParser(description='Visualize interpretable decision trees')
    parser.add_argument('--tree-dir', type=str, default='models/interpretable',
                       help='Directory containing trained trees')
    parser.add_argument('--output-dir', type=str, default='visualizations/trees',
                       help='Directory to save visualizations')
    parser.add_argument('--format', type=str, choices=['all', 'png', 'text', 'markdown'], 
                       default='all', help='Visualization format to generate')
    
    args = parser.parse_args()
    
    print(f"Loading trees from {args.tree_dir}")
    
    # Load trees
    trainer = InterpretableTreeTrainer()
    trees = trainer.load_trees(args.tree_dir)
    
    if not trees:
        print("No trees found to visualize")
        return
    
    print(f"Found {len(trees)} trees to visualize")
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Generate visualizations based on format
    if args.format in ['all', 'png']:
        print("Generating PNG visualizations...")
        for street, tree in trees.items():
            if tree is not None:
                from src.interpretable.visualizer import visualize_tree
                from src.interpretable.feature_extractor import get_feature_names
                
                feature_names = get_feature_names()
                output_path = os.path.join(args.output_dir, f'{street}_tree')
                png_path = visualize_tree(tree, feature_names, output_path, street)
                if png_path:
                    print(f"  {street}: {png_path}")
    
    if args.format in ['all', 'text']:
        print("Generating text rules...")
        for street, tree in trees.items():
            if tree is not None:
                from src.interpretable.visualizer import export_tree_as_text
                from src.interpretable.feature_extractor import get_feature_names
                
                feature_names = get_feature_names()
                text_path = os.path.join(args.output_dir, f'{street}_rules.txt')
                export_tree_as_text(tree, feature_names, text_path)
                print(f"  {street}: {text_path}")
    
    if args.format in ['all', 'markdown']:
        print("Generating markdown documentation...")
        for street, tree in trees.items():
            if tree is not None:
                from src.interpretable.visualizer import export_tree_as_markdown
                from src.interpretable.feature_extractor import get_feature_names
                
                feature_names = get_feature_names()
                md_path = os.path.join(args.output_dir, f'{street}_rules.md')
                export_tree_as_markdown(tree, feature_names, md_path, street)
                print(f"  {street}: {md_path}")
    
    # Create comprehensive strategy chart
    print("Creating strategy chart...")
    strategy_path = create_strategy_chart(trees, os.path.join(args.output_dir, 'strategy_chart.md'))
    if strategy_path:
        print(f"  Strategy chart: {strategy_path}")
    
    print(f"\nAll visualizations saved to {args.output_dir}")
    print("Files generated:")
    for file in os.listdir(args.output_dir):
        print(f"  - {file}")

if __name__ == "__main__":
    main()

