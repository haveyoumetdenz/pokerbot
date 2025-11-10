"""
Tree visualization tools for interpretable poker AI.
Exports decision trees in multiple formats for analysis and teaching.
"""

import os
import numpy as np
from typing import Dict, List, Any, Optional
from sklearn.tree import export_graphviz, export_text
from sklearn.tree import DecisionTreeClassifier

# Optional graphviz import
try:
    import graphviz
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("Warning: graphviz not available. Tree visualization will be limited.")

from .feature_extractor import get_feature_names

def visualize_tree(tree: DecisionTreeClassifier, feature_names: List[str], 
                   output_path: str, street: str = "unknown") -> str:
    """
    Export tree as visual diagram using Graphviz.
    
    Args:
        tree: Trained decision tree
        feature_names: List of feature names
        output_path: Path to save the visualization (without extension)
        street: Name of the street for title
        
    Returns:
        Path to the generated image file
    """
    if not GRAPHVIZ_AVAILABLE:
        print(f"Graphviz not available. Skipping visualization for {street}")
        return None
        
    try:
        # Export tree as DOT format
        dot_data = export_graphviz(
            tree,
            feature_names=feature_names,
            class_names=['fold', 'call', 'raise'],
            filled=True,
            rounded=True,
            special_characters=True,
            max_depth=10,  # Limit depth for readability
            fontname="Arial",
            fontsize=10
        )
        
        # Create graph
        graph = graphviz.Source(dot_data)
        
        # Render as PNG
        image_path = graph.render(output_path, format='png', cleanup=True)
        
        print(f"Tree visualization saved to {image_path}")
        return image_path
        
    except Exception as e:
        print(f"Error creating tree visualization: {e}")
        return None

def export_tree_as_text(tree: DecisionTreeClassifier, feature_names: List[str], 
                       output_path: str) -> str:
    """
    Export tree as text rules.
    
    Args:
        tree: Trained decision tree
        feature_names: List of feature names
        output_path: Path to save the text file
        
    Returns:
        Path to the generated text file
    """
    try:
        # Export tree as text
        tree_rules = export_text(
            tree,
            feature_names=feature_names,
            max_depth=10,
            spacing=3,
            decimals=3
        )
        
        # Save to file
        with open(output_path, 'w') as f:
            f.write(f"Decision Tree Rules\n")
            f.write(f"==================\n\n")
            f.write(tree_rules)
        
        print(f"Tree rules saved to {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error exporting tree as text: {e}")
        return None

def export_tree_as_markdown(tree: DecisionTreeClassifier, feature_names: List[str], 
                           output_path: str, street: str = "unknown") -> str:
    """
    Export tree as markdown table with readable rules.
    
    Args:
        tree: Trained decision tree
        feature_names: List of feature names
        output_path: Path to save the markdown file
        street: Name of the street for title
        
    Returns:
        Path to the generated markdown file
    """
    try:
        # Generate decision rules
        rules = _generate_decision_rules(tree, feature_names)
        
        # Create markdown content
        markdown_content = f"""# {street.title()} Decision Tree Rules

## Overview
This document contains the decision rules learned by the interpretable poker AI for {street} betting rounds.

## Feature Descriptions
{_get_feature_descriptions()}

## Decision Rules

"""
        
        # Add rules
        for i, rule in enumerate(rules, 1):
            markdown_content += f"### Rule {i}: {rule['action'].upper()}\n"
            markdown_content += f"**Conditions:** {rule['conditions']}\n"
            markdown_content += f"**Samples:** {rule['samples']}\n"
            markdown_content += f"**Confidence:** {rule['confidence']:.1%}\n\n"
        
        # Add feature importance
        markdown_content += "## Feature Importance\n\n"
        importances = tree.feature_importances_
        importance_pairs = list(zip(feature_names, importances))
        importance_pairs.sort(key=lambda x: x[1], reverse=True)
        
        markdown_content += "| Feature | Importance |\n"
        markdown_content += "|---------|------------|\n"
        for feature, importance in importance_pairs[:10]:  # Top 10 features
            if importance > 0:
                markdown_content += f"| {feature} | {importance:.3f} |\n"
        
        # Save to file
        with open(output_path, 'w') as f:
            f.write(markdown_content)
        
        print(f"Tree markdown saved to {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error exporting tree as markdown: {e}")
        return None

def _generate_decision_rules(tree: DecisionTreeClassifier, feature_names: List[str]) -> List[Dict[str, Any]]:
    """Generate human-readable decision rules from the tree."""
    rules = []
    
    # Get tree structure
    tree_ = tree.tree_
    feature_names = feature_names if feature_names else [f"feature_{i}" for i in range(tree_.n_features)]
    
    def extract_rules(node_id, conditions, depth=0):
        if tree_.feature[node_id] != -2:  # Not a leaf
            feature_name = feature_names[tree_.feature[node_id]]
            threshold = tree_.threshold[node_id]
            
            # Left child (<= threshold)
            left_conditions = conditions + [f"{feature_name} <= {threshold:.3f}"]
            extract_rules(tree_.children_left[node_id], left_conditions, depth + 1)
            
            # Right child (> threshold)
            right_conditions = conditions + [f"{feature_name} > {threshold:.3f}"]
            extract_rules(tree_.children_right[node_id], right_conditions, depth + 1)
        else:
            # Leaf node
            class_counts = tree_.value[node_id][0]
            total_samples = sum(class_counts)
            
            if total_samples > 0:
                # Find the most common class
                class_idx = np.argmax(class_counts)
                class_names = ['fold', 'call', 'raise']
                action = class_names[class_idx] if class_idx < len(class_names) else 'unknown'
                
                confidence = class_counts[class_idx] / total_samples
                
                rules.append({
                    'action': action,
                    'conditions': ' AND '.join(conditions),
                    'samples': int(total_samples),
                    'confidence': confidence
                })
    
    # Extract rules starting from root
    extract_rules(0, [])
    
    # Sort by confidence and sample count
    rules.sort(key=lambda x: (x['confidence'], x['samples']), reverse=True)
    
    return rules[:20]  # Return top 20 rules

def _get_feature_descriptions() -> str:
    """Get human-readable descriptions of features."""
    descriptions = {
        'hand_equity': 'Probability of winning the hand (0-1)',
        'equity_percentile': 'Percentile rank of hand strength vs random hands (0-100)',
        'pot_size_bb': 'Pot size in big blinds',
        'current_bet_bb': 'Current bet amount in big blinds',
        'total_street_bets': 'Number of bets made this street',
        'num_raises_this_street': 'Number of raises made this street',
        'pot_odds': 'Pot odds for calling (0-1)',
        'position_numeric': 'Position at table (0=blinds, 1=early, 2=middle, 3=late)',
        'players_remaining': 'Number of active players',
        'position_relative_button': 'Position relative to button (0-5)',
        'stack_size_bb': 'Stack size in big blinds',
        'effective_stack': 'Effective stack size (minimum among active players)',
        'stack_to_pot_ratio': 'Ratio of stack size to pot size',
        'street_numeric': 'Betting round (0=preflop, 1=flop, 2=turn, 3=river)',
        'is_blind': 'Whether player is in small or big blind position',
        'is_button': 'Whether player is on the button',
        'players_to_act': 'Number of players who still need to act',
        'has_been_raised': 'Whether there has been a raise this street',
        'num_callers': 'Number of players who have called this street',
        'aggression_factor': 'Measure of betting aggression this street',
        'pot_commitment': 'Percentage of pot already committed by player',
        'fold_equity': 'Estimated probability opponents will fold'
    }
    
    markdown = "| Feature | Description |\n"
    markdown += "|---------|-------------|\n"
    
    for feature, description in descriptions.items():
        markdown += f"| {feature} | {description} |\n"
    
    return markdown

def create_tree_summary(tree: DecisionTreeClassifier, street: str) -> Dict[str, Any]:
    """Create a summary of the tree for analysis."""
    return {
        'street': street,
        'depth': tree.get_depth(),
        'n_leaves': tree.get_n_leaves(),
        'n_features': tree.n_features_in_,
        'feature_importance': dict(zip(tree.feature_names_in_, tree.feature_importances_)),
        'class_distribution': dict(zip(tree.classes_, tree.tree_.value[0][0]))
    }

def visualize_all_trees(trees: Dict[str, DecisionTreeClassifier], 
                       output_dir: str = 'visualizations/trees') -> Dict[str, str]:
    """
    Visualize all trees in multiple formats.
    
    Args:
        trees: Dictionary mapping street names to trees
        output_dir: Directory to save visualizations
        
    Returns:
        Dictionary mapping street names to output file paths
    """
    os.makedirs(output_dir, exist_ok=True)
    
    feature_names = get_feature_names()
    output_paths = {}
    
    for street, tree in trees.items():
        if tree is None:
            continue
        
        print(f"Visualizing {street} tree...")
        
        # Create visualizations
        base_path = os.path.join(output_dir, street)
        
        # PNG visualization
        png_path = visualize_tree(tree, feature_names, base_path, street)
        if png_path:
            output_paths[f'{street}_png'] = png_path
        
        # Text rules
        text_path = export_tree_as_text(tree, feature_names, f"{base_path}.txt")
        if text_path:
            output_paths[f'{street}_text'] = text_path
        
        # Markdown rules
        md_path = export_tree_as_markdown(tree, feature_names, f"{base_path}.md", street)
        if md_path:
            output_paths[f'{street}_markdown'] = md_path
    
    return output_paths

def create_strategy_chart(trees: Dict[str, DecisionTreeClassifier], 
                         output_path: str = 'visualizations/strategy_chart.md') -> str:
    """
    Create a comprehensive strategy chart showing opening ranges and betting patterns.
    
    Args:
        trees: Dictionary mapping street names to trees
        output_path: Path to save the strategy chart
        
    Returns:
        Path to the generated strategy chart
    """
    try:
        content = """# Poker Strategy Chart - Interpretable AI

## Overview
This chart summarizes the strategy learned by the interpretable poker AI across all betting rounds.

## Opening Ranges by Position

### Preflop Strategy
"""
        
        # Add preflop strategy if available
        if 'preflop' in trees and trees['preflop'] is not None:
            preflop_rules = _generate_decision_rules(trees['preflop'], get_feature_names())
            content += "#### Early Position\n"
            content += "- Tight range: Premium hands only\n"
            content += "- Fold most hands, raise with strong hands\n\n"
            
            content += "#### Middle Position\n"
            content += "- Moderate range: Good hands and some speculative hands\n"
            content += "- Call with medium strength, raise with strong hands\n\n"
            
            content += "#### Late Position\n"
            content += "- Wide range: Can play more hands due to position\n"
            content += "- Steal blinds with weaker hands\n\n"
        
        # Add postflop strategies
        for street in ['flop', 'turn', 'river']:
            if street in trees and trees[street] is not None:
                content += f"### {street.title()} Strategy\n"
                content += f"#### Key Factors\n"
                content += f"- Hand equity is the primary factor\n"
                content += f"- Pot odds determine calling decisions\n"
                content += f"- Position affects betting frequency\n\n"
        
        # Add general principles
        content += """## General Principles

### Value Betting
- Bet for value when you have a strong hand
- Size bets to get called by weaker hands
- Consider opponent's likely range

### Bluffing
- Bluff when you have fold equity
- Use position to your advantage
- Consider pot odds and stack sizes

### Pot Odds
- Call when pot odds are favorable
- Fold when pot odds are unfavorable
- Consider implied odds for future streets

## Feature Importance Summary

The AI considers these factors in order of importance:
1. Hand equity - Probability of winning
2. Pot odds - Ratio of pot to call amount
3. Position - Table position relative to button
4. Stack size - Effective stack size
5. Betting history - Previous actions this street

## Decision Tree Statistics

"""
        
        # Add tree statistics
        for street, tree in trees.items():
            if tree is not None:
                content += f"### {street.title()}\n"
                content += f"- Tree depth: {tree.get_depth()}\n"
                content += f"- Number of leaves: {tree.get_n_leaves()}\n"
                content += f"- Features used: {tree.n_features_in_}\n\n"
        
        # Save to file
        with open(output_path, 'w') as f:
            f.write(content)
        
        print(f"Strategy chart saved to {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error creating strategy chart: {e}")
        return None

def main():
    """Main function for tree visualization."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Visualize interpretable decision trees')
    parser.add_argument('--tree-dir', type=str, default='models/interpretable',
                       help='Directory containing trained trees')
    parser.add_argument('--output-dir', type=str, default='visualizations/trees',
                       help='Directory to save visualizations')
    
    args = parser.parse_args()
    
    # Load trees
    from .tree_trainer import InterpretableTreeTrainer
    trainer = InterpretableTreeTrainer()
    trees = trainer.load_trees(args.tree_dir)
    
    if not trees:
        print("No trees found to visualize")
        return
    
    # Create visualizations
    output_paths = visualize_all_trees(trees, args.output_dir)
    
    # Create strategy chart
    strategy_path = create_strategy_chart(trees, os.path.join(args.output_dir, 'strategy_chart.md'))
    
    print(f"Visualizations saved to {args.output_dir}")
    print(f"Strategy chart saved to {strategy_path}")

if __name__ == "__main__":
    main()
