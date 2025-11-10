"""
Data collection infrastructure for interpretable poker AI.
Collects (state, action, value) tuples during CFR training with interpretable features.
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import pokers as pkrs
from .feature_extractor import extract_interpretable_features, features_to_vector

class InterpretableDataCollector:
    """Collects interpretable decision data during CFR training."""
    
    def __init__(self, output_dir: str = 'data/interpretable'):
        self.output_dir = output_dir
        self.datasets = {
            'preflop': [],
            'flop': [],
            'turn': [],
            'river': []
        }
        self.stats = {
            'total_decisions': 0,
            'decisions_by_street': {'preflop': 0, 'flop': 0, 'turn': 0, 'river': 0},
            'actions_taken': {'fold': 0, 'call': 0, 'raise': 0}
        }
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def record_decision(self, state: pkrs.State, player_id: int, action: pkrs.Action, 
                      expected_value: float, iteration: int = 0) -> None:
        """
        Record a decision point with interpretable features.
        
        Args:
            state: Current poker state
            player_id: ID of the player making the decision
            action: Action taken by the player
            expected_value: Expected value of the decision
            iteration: Training iteration number
        """
        try:
            # Extract interpretable features
            features = extract_interpretable_features(state, player_id)
            street = features['street']
            
            # Convert action to category
            action_category = self._action_to_category(action)
            
            # Create decision record
            decision_record = {
                'iteration': iteration,
                'player_id': player_id,
                'features': features,
                'action': action_category,
                'bet_size': action.amount if action.action == pkrs.ActionEnum.Raise else 0.0,
                'expected_value': expected_value,
                'pot_size': state.pot,
                'stack_size': state.players_state[player_id].stake,
                'position': features['position'],
                'hand_equity': features['hand_equity'],
                'pot_odds': features['pot_odds']
            }
            
            # Add to appropriate dataset
            if street in self.datasets:
                self.datasets[street].append(decision_record)
                self.stats['decisions_by_street'][street] += 1
                self.stats['actions_taken'][action_category] += 1
                self.stats['total_decisions'] += 1
            
        except Exception as e:
            print(f"Warning: Failed to record decision: {e}")
    
    def _action_to_category(self, action: pkrs.Action) -> str:
        """Convert pokers action to category string."""
        if action.action == pkrs.ActionEnum.Fold:
            return 'fold'
        elif action.action == pkrs.ActionEnum.Check or action.action == pkrs.ActionEnum.Call:
            return 'call'
        elif action.action == pkrs.ActionEnum.Raise:
            return 'raise'
        else:
            return 'fold'  # Default to fold for unknown actions
    
    def save_datasets(self) -> None:
        """Save collected data as CSV files."""
        print(f"Saving interpretable datasets to {self.output_dir}")
        
        for street, data in self.datasets.items():
            if not data:
                print(f"Warning: No data collected for {street}")
                continue
                
            # Convert to DataFrame
            df = self._prepare_dataframe(data)
            
            # Save CSV
            output_path = os.path.join(self.output_dir, f'{street}_decisions.csv')
            df.to_csv(output_path, index=False)
            print(f"Saved {len(df)} decisions for {street} to {output_path}")
        
        # Save statistics
        self._save_statistics()
    
    def _prepare_dataframe(self, data: List[Dict]) -> pd.DataFrame:
        """Prepare data for DataFrame conversion."""
        if not data:
            return pd.DataFrame()
        
        # Extract features into separate columns
        records = []
        for record in data:
            features = record['features']
            record_flat = {
                'iteration': record['iteration'],
                'player_id': record['player_id'],
                'action': record['action'],
                'bet_size': record['bet_size'],
                'expected_value': record['expected_value'],
                'pot_size': record['pot_size'],
                'stack_size': record['stack_size'],
                'position': record['position'],
                'hand_equity': record['hand_equity'],
                'pot_odds': record['pot_odds']
            }
            
            # Add all feature columns
            for key, value in features.items():
                if isinstance(value, (int, float)):
                    record_flat[f'feature_{key}'] = value
                else:
                    # Convert non-numeric features to numeric
                    record_flat[f'feature_{key}'] = self._convert_to_numeric(value)
            
            records.append(record_flat)
        
        return pd.DataFrame(records)
    
    def _convert_to_numeric(self, value: Any) -> float:
        """Convert non-numeric values to numeric for DataFrame."""
        if isinstance(value, (int, float)):
            return float(value)
        elif isinstance(value, str):
            # Convert string categories to numeric
            if value in ['blinds', 'early', 'middle', 'late']:
                return {'blinds': 0, 'early': 1, 'middle': 2, 'late': 3}[value]
            elif value in ['preflop', 'flop', 'turn', 'river', 'showdown']:
                return {'preflop': 0, 'flop': 1, 'turn': 2, 'river': 3, 'showdown': 4}[value]
            else:
                return 0.0
        else:
            return 0.0
    
    def _save_statistics(self) -> None:
        """Save collection statistics."""
        stats_path = os.path.join(self.output_dir, 'collection_stats.json')
        
        import json
        with open(stats_path, 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        print(f"Saved collection statistics to {stats_path}")
    
    def get_dataset_summary(self) -> Dict[str, Any]:
        """Get summary of collected datasets."""
        summary = {
            'total_decisions': self.stats['total_decisions'],
            'decisions_by_street': self.stats['decisions_by_street'].copy(),
            'actions_taken': self.stats['actions_taken'].copy(),
            'dataset_sizes': {}
        }
        
        for street, data in self.datasets.items():
            summary['dataset_sizes'][street] = len(data)
        
        return summary
    
    def clear_data(self) -> None:
        """Clear all collected data."""
        for street in self.datasets:
            self.datasets[street] = []
        
        self.stats = {
            'total_decisions': 0,
            'decisions_by_street': {'preflop': 0, 'flop': 0, 'turn': 0, 'river': 0},
            'actions_taken': {'fold': 0, 'call': 0, 'raise': 0}
        }
    
    def load_datasets(self) -> Dict[str, pd.DataFrame]:
        """Load previously saved datasets."""
        datasets = {}
        
        for street in ['preflop', 'flop', 'turn', 'river']:
            file_path = os.path.join(self.output_dir, f'{street}_decisions.csv')
            if os.path.exists(file_path):
                datasets[street] = pd.read_csv(file_path)
                print(f"Loaded {len(datasets[street])} decisions for {street}")
            else:
                print(f"No data file found for {street}")
                datasets[street] = pd.DataFrame()
        
        return datasets

# Global data collector instance
_data_collector = None

def get_data_collector(output_dir: str = 'data/interpretable') -> InterpretableDataCollector:
    """Get global data collector instance."""
    global _data_collector
    if _data_collector is None:
        _data_collector = InterpretableDataCollector(output_dir)
    return _data_collector

def record_decision(state: pkrs.State, player_id: int, action: pkrs.Action, 
                   expected_value: float, iteration: int = 0) -> None:
    """Convenience function to record a decision."""
    get_data_collector().record_decision(state, player_id, action, expected_value, iteration)

