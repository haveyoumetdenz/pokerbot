"""
Decision tree trainer for interpretable poker AI.
Trains decision trees on collected CFR data for each betting round.
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

from .feature_extractor import get_feature_names, features_to_vector

class InterpretableTreeTrainer:
    """Trains decision trees for interpretable poker AI."""
    
    def __init__(self, max_depth: int = 12, min_samples_split: int = 100, 
                 min_samples_leaf: int = 50):
        self.trees = {}  # One tree per street
        self.feature_names = get_feature_names()
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.training_stats = {}
        
    def train_tree_for_street(self, street_data: pd.DataFrame, street: str, 
                             max_depth: Optional[int] = None) -> DecisionTreeClassifier:
        """
        Train a decision tree for one betting round.
        
        Args:
            street_data: DataFrame with training data for the street
            street: Name of the street (preflop, flop, turn, river)
            max_depth: Maximum tree depth (uses default if None)
            
        Returns:
            Trained decision tree classifier
        """
        if street_data.empty:
            print(f"Warning: No data available for {street}")
            return None
        
        print(f"Training tree for {street} with {len(street_data)} samples...")
        
        # Prepare feature matrix and labels
        X, y = self._prepare_training_data(street_data)
        
        if len(X) == 0:
            print(f"Warning: No valid features for {street}")
            return None
        
        # Split for validation
        if len(X) > 20:  # Only split if we have enough data
            X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        else:
            X_train, X_val, y_train, y_val = X, X, y, y
        
        # Use improved parameters for better performance
        # Deeper trees with better regularization
        if max_depth is None:
            max_depth = self.max_depth
        
        # Improved parameter grid for better performance
        param_grid = {
            'max_depth': [max_depth, max_depth + 2, max_depth + 4] if max_depth < 20 else [max_depth],
            'min_samples_split': [20, 50, 100],
            'min_samples_leaf': [10, 25, 50]
        }
        
        tree = DecisionTreeClassifier(
            criterion='gini',
            random_state=42,
            class_weight='balanced'  # Handle class imbalance
        )
        
        # Use grid search if we have enough data
        if len(X_train) > 100:
            clf = GridSearchCV(
                tree, param_grid, cv=min(5, len(X_train)//20), 
                scoring='accuracy', n_jobs=-1, verbose=0
            )
            clf.fit(X_train, y_train)
            best_tree = clf.best_estimator_
            best_params = clf.best_params_
        elif len(X_train) > 50:
            # Use moderate parameters for medium datasets
            best_tree = DecisionTreeClassifier(
                criterion='gini',
                max_depth=max_depth,
                min_samples_split=50,
                min_samples_leaf=25,
                random_state=42,
                class_weight='balanced'
            )
            best_tree.fit(X_train, y_train)
            best_params = {'max_depth': max_depth, 'min_samples_split': 50, 'min_samples_leaf': 25}
        else:
            # Use default parameters for small datasets
            best_tree = DecisionTreeClassifier(
                criterion='gini',
                max_depth=min(max_depth, 8),
                min_samples_split=20,
                min_samples_leaf=10,
                random_state=42,
                class_weight='balanced'
            )
            best_tree.fit(X_train, y_train)
            best_params = {'max_depth': min(max_depth, 8), 'min_samples_split': 20, 'min_samples_leaf': 10}
        
        # Store feature names for better interpretability
        # This ensures the tree knows which features it was trained with
        if hasattr(best_tree, 'feature_names_in_'):
            # sklearn >= 1.0 automatically stores feature names
            pass
        else:
            # For older sklearn versions, we'll extract feature names manually
            # The feature names are already in self.feature_names
            pass
        
        # Evaluate performance
        train_accuracy = best_tree.score(X_train, y_train)
        val_accuracy = best_tree.score(X_val, y_val) if len(X_val) > 0 else train_accuracy
        
        # Store feature names in the tree for later use
        # This helps with feature matching when loading trees
        if hasattr(best_tree, 'feature_names_in_'):
            # sklearn >= 1.0: feature names are automatically stored
            pass
        else:
            # For older sklearn versions, we can't directly set feature_names_in_
            # But we can ensure the tree knows the number of features
            pass
        
        # Store training statistics
        self.training_stats[street] = {
            'train_accuracy': train_accuracy,
            'val_accuracy': val_accuracy,
            'best_params': best_params,
            'n_samples': len(X),
            'n_features': X.shape[1],
            'tree_depth': best_tree.get_depth(),
            'n_leaves': best_tree.get_n_leaves(),
            'feature_count': X.shape[1]
        }
        
        print(f"{street} tree: depth={best_tree.get_depth()}, "
              f"features={X.shape[1]}, "
              f"train_acc={train_accuracy:.3f}, val_acc={val_accuracy:.3f}")
        
        # Print feature importance
        self._print_feature_importance(best_tree, street)
        
        self.trees[street] = best_tree
        return best_tree
    
    def _prepare_training_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare feature matrix and labels from DataFrame."""
        # Extract feature columns - ensure we use ALL features from data
        feature_cols = [col for col in data.columns if col.startswith('feature_')]
        
        # Sort feature columns to match feature_names order
        # This ensures consistency with get_feature_names()
        feature_names_expected = [f'feature_{name}' for name in self.feature_names]
        feature_cols_sorted = []
        for expected_name in feature_names_expected:
            if expected_name in feature_cols:
                feature_cols_sorted.append(expected_name)
        
        # Add any extra features that weren't in expected list
        for col in feature_cols:
            if col not in feature_cols_sorted:
                feature_cols_sorted.append(col)
        
        if not feature_cols_sorted:
            print("Warning: No feature columns found in data")
            return np.array([]), np.array([])
        
        print(f"  Using {len(feature_cols_sorted)} features for training")
        
        # Create feature matrix
        X = data[feature_cols_sorted].values
        
        # Convert to numeric and handle missing values
        try:
            X = X.astype(np.float32)
        except (ValueError, TypeError):
            # Handle non-numeric data
            X_clean = []
            for i in range(X.shape[0]):
                row = []
                for j in range(X.shape[1]):
                    try:
                        val = float(X[i, j])
                        row.append(val)
                    except (ValueError, TypeError):
                        row.append(0.0)  # Default value for non-numeric
                X_clean.append(row)
            X = np.array(X_clean, dtype=np.float32)
        
        # Handle missing values
        X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
        
        # Extract labels
        if 'action' in data.columns:
            y = data['action'].values
        else:
            print("Warning: No action column found in data")
            return np.array([]), np.array([])
        
        # Remove rows with invalid data (check for NaN after conversion)
        try:
            valid_mask = ~np.isnan(X).any(axis=1)
        except TypeError:
            # If still having issues, just use all rows
            valid_mask = np.ones(X.shape[0], dtype=bool)
        
        X = X[valid_mask]
        y = y[valid_mask]
        
        return X, y
    
    def _print_feature_importance(self, tree: DecisionTreeClassifier, street: str) -> None:
        """Print feature importance for the trained tree."""
        importances = tree.feature_importances_
        
        # Get feature names (handle different sklearn versions)
        if hasattr(tree, 'feature_names_in_'):
            feature_cols = [name for name in self.feature_names if name in tree.feature_names_in_]
        else:
            # Fallback for older sklearn versions
            feature_cols = [f"feature_{i}" for i in range(len(importances))]
        
        if not feature_cols:
            feature_cols = [f"feature_{i}" for i in range(len(importances))]
        
        # Sort by importance
        importance_pairs = list(zip(feature_cols, importances))
        importance_pairs.sort(key=lambda x: x[1], reverse=True)
        
        print(f"Top 5 features for {street}:")
        for i, (feature, importance) in enumerate(importance_pairs[:5]):
            if importance > 0:
                print(f"  {i+1}. {feature}: {importance:.3f}")
    
    def train_all_trees(self, data_dir: str = 'data/interpretable') -> Dict[str, DecisionTreeClassifier]:
        """
        Train trees for all betting rounds.
        
        Args:
            data_dir: Directory containing CSV files with training data
            
        Returns:
            Dictionary mapping street names to trained trees
        """
        print(f"Training decision trees from data in {data_dir}")
        
        streets = ['preflop', 'flop', 'turn', 'river']
        
        for street in streets:
            file_path = os.path.join(data_dir, f'{street}_decisions.csv')
            
            if os.path.exists(file_path):
                try:
                    data = pd.read_csv(file_path)
                    tree = self.train_tree_for_street(data, street)
                    if tree is not None:
                        self.trees[street] = tree
                except Exception as e:
                    print(f"Error training tree for {street}: {e}")
            else:
                print(f"No data file found for {street}: {file_path}")
        
        print(f"Successfully trained {len(self.trees)} trees")
        return self.trees
    
    def save_trees(self, output_dir: str = 'models/interpretable') -> None:
        """Save trained trees using joblib."""
        os.makedirs(output_dir, exist_ok=True)
        
        for street, tree in self.trees.items():
            if tree is not None:
                tree_path = os.path.join(output_dir, f'{street}_tree.pkl')
                joblib.dump(tree, tree_path)
                print(f"Saved {street} tree to {tree_path}")
        
        # Save training statistics (convert numpy types to Python types)
        stats_path = os.path.join(output_dir, 'training_stats.json')
        import json
        
        # Convert numpy types to Python types for JSON serialization
        def convert_numpy_types(obj):
            if isinstance(obj, dict):
                return {key: convert_numpy_types(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(item) for item in obj]
            elif hasattr(obj, 'item'):  # numpy scalar
                return obj.item()
            elif hasattr(obj, 'tolist'):  # numpy array
                return obj.tolist()
            else:
                return obj
        
        converted_stats = convert_numpy_types(self.training_stats)
        
        with open(stats_path, 'w') as f:
            json.dump(converted_stats, f, indent=2)
        print(f"Saved training statistics to {stats_path}")
    
    def load_trees(self, tree_dir: str = 'models/interpretable') -> Dict[str, DecisionTreeClassifier]:
        """Load previously trained trees."""
        self.trees = {}
        
        streets = ['preflop', 'flop', 'turn', 'river']
        
        for street in streets:
            tree_path = os.path.join(tree_dir, f'{street}_tree.pkl')
            if os.path.exists(tree_path):
                try:
                    self.trees[street] = joblib.load(tree_path)
                    print(f"Loaded {street} tree from {tree_path}")
                except Exception as e:
                    print(f"Error loading tree for {street}: {e}")
            else:
                print(f"No tree file found for {street}: {tree_path}")
        
        # Load training statistics if available
        stats_path = os.path.join(tree_dir, 'training_stats.json')
        if os.path.exists(stats_path):
            try:
                import json
                with open(stats_path, 'r') as f:
                    self.training_stats = json.load(f)
                print(f"Loaded training statistics from {stats_path}")
            except Exception as e:
                print(f"Error loading training statistics: {e}")
        
        return self.trees
    
    def evaluate_trees(self, data_dir: str = 'data/interpretable') -> Dict[str, Dict]:
        """Evaluate performance of all trained trees."""
        evaluation_results = {}
        
        for street, tree in self.trees.items():
            if tree is None:
                continue
                
            file_path = os.path.join(data_dir, f'{street}_decisions.csv')
            if not os.path.exists(file_path):
                continue
            
            try:
                data = pd.read_csv(file_path)
                X, y = self._prepare_training_data(data)
                
                if len(X) == 0:
                    continue
                
                # Predictions
                y_pred = tree.predict(X)
                
                # Calculate metrics
                accuracy = accuracy_score(y, y_pred)
                
                # Classification report
                report = classification_report(y, y_pred, output_dict=True)
                
                # Confusion matrix
                cm = confusion_matrix(y, y_pred)
                
                evaluation_results[street] = {
                    'accuracy': accuracy,
                    'classification_report': report,
                    'confusion_matrix': cm.tolist(),
                    'n_samples': len(X),
                    'tree_depth': tree.get_depth(),
                    'n_leaves': tree.get_n_leaves()
                }
                
                print(f"{street} evaluation: accuracy={accuracy:.3f}, "
                      f"depth={tree.get_depth()}, leaves={tree.get_n_leaves()}")
                
            except Exception as e:
                print(f"Error evaluating {street} tree: {e}")
        
        return evaluation_results
    
    def get_tree_summary(self) -> Dict[str, Any]:
        """Get summary of all trained trees."""
        summary = {
            'n_trees': len(self.trees),
            'streets': list(self.trees.keys()),
            'training_stats': self.training_stats
        }
        
        for street, tree in self.trees.items():
            if tree is not None:
                summary[f'{street}_depth'] = tree.get_depth()
                summary[f'{street}_leaves'] = tree.get_n_leaves()
        
        return summary

def train_interpretable_trees(data_dir: str = 'data/interpretable', 
                            output_dir: str = 'models/interpretable',
                            max_depth: int = 12) -> InterpretableTreeTrainer:
    """
    Convenience function to train all interpretable trees.
    
    Args:
        data_dir: Directory containing training data
        output_dir: Directory to save trained trees
        max_depth: Maximum tree depth
        
    Returns:
        Trained InterpretableTreeTrainer
    """
    trainer = InterpretableTreeTrainer(max_depth=max_depth)
    trainer.train_all_trees(data_dir)
    trainer.save_trees(output_dir)
    
    # Print summary
    summary = trainer.get_tree_summary()
    print(f"\nTraining Summary:")
    print(f"Trees trained: {summary['n_trees']}")
    print(f"Streets: {summary['streets']}")
    
    return trainer

def main():
    """Main function for training interpretable trees."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Train interpretable decision trees')
    parser.add_argument('--data-dir', type=str, default='data/interpretable', 
                       help='Directory containing training data')
    parser.add_argument('--output-dir', type=str, default='models/interpretable',
                       help='Directory to save trained trees')
    parser.add_argument('--max-depth', type=int, default=12,
                       help='Maximum tree depth')
    
    args = parser.parse_args()
    
    # Train trees
    trainer = train_interpretable_trees(
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        max_depth=args.max_depth
    )
    
    print("Tree training completed successfully!")

if __name__ == "__main__":
    main()
