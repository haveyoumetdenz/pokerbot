"""
Interpretable poker agent using decision trees.
Uses trained decision trees to make poker decisions with explanations.
"""

import os
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
import pokers as pkrs
from sklearn.tree import DecisionTreeClassifier
import joblib

from .feature_extractor import extract_interpretable_features, features_to_vector, get_feature_names
from .tree_trainer import InterpretableTreeTrainer

class InterpretablePokerAgent:
    """Poker agent that uses decision trees for interpretable action selection."""
    
    def __init__(self, player_id: int = 0, tree_dir: str = 'models/interpretable'):
        self.player_id = player_id
        self.tree_dir = tree_dir
        self.trees = {}
        self.feature_names = get_feature_names()
        self.decision_history = []
        
        # Cumulative betting history across games
        self.betting_history = {
            'game_count': 0,
            'current_game': [],
            'opponent_stats': {},  # Per-opponent statistics
            'street_stats': {
                'preflop': {'raises': 0, 'calls': 0, 'folds': 0, 'total': 0},
                'flop': {'raises': 0, 'calls': 0, 'folds': 0, 'total': 0},
                'turn': {'raises': 0, 'calls': 0, 'folds': 0, 'total': 0},
                'river': {'raises': 0, 'calls': 0, 'folds': 0, 'total': 0}
            },
            'recent_actions': []  # Last N actions for pattern detection
        }
        
        # Load trees
        self.load_trees()
    
    def load_trees(self) -> Dict[str, DecisionTreeClassifier]:
        """Load trained decision trees."""
        streets = ['preflop', 'flop', 'turn', 'river']
        
        for street in streets:
            tree_path = os.path.join(self.tree_dir, f'{street}_tree.pkl')
            if os.path.exists(tree_path):
                try:
                    self.trees[street] = joblib.load(tree_path)
                    print(f"Loaded {street} tree from {tree_path}")
                except Exception as e:
                    print(f"Error loading tree for {street}: {e}")
            else:
                print(f"No tree file found for {street}: {tree_path}")
        
        return self.trees
    
    def start_new_game(self):
        """Initialize betting history for a new game."""
        self.betting_history['game_count'] += 1
        self.betting_history['current_game'] = []
    
    def record_action(self, state: pkrs.State, player_id: int, action: pkrs.Action):
        """Record an action for betting history tracking."""
        try:
            # Get current street
            street_names = ['preflop', 'flop', 'turn', 'river', 'showdown']
            street = street_names[int(state.stage)] if int(state.stage) < len(street_names) else 'preflop'
            
            # Determine action type
            if action.action == pkrs.ActionEnum.Fold:
                action_type = 'fold'
            elif action.action in [pkrs.ActionEnum.Check, pkrs.ActionEnum.Call]:
                action_type = 'call'
            elif action.action == pkrs.ActionEnum.Raise:
                action_type = 'raise'
            else:
                action_type = 'unknown'
            
            # Record action
            action_record = {
                'player_id': player_id,
                'street': street,
                'action': action_type,
                'bet_amount': action.amount if hasattr(action, 'amount') else 0,
                'pot_size': state.pot,
                'game_num': self.betting_history['game_count']
            }
            
            self.betting_history['current_game'].append(action_record)
            
            # Update cumulative statistics (only for completed streets)
            if street in self.betting_history['street_stats']:
                # Map action_type to dictionary key (plural form)
                action_key_map = {
                    'raise': 'raises',
                    'call': 'calls',
                    'fold': 'folds'
                }
                if action_type in action_key_map:
                    action_key = action_key_map[action_type]
                    if action_key in self.betting_history['street_stats'][street]:
                        self.betting_history['street_stats'][street][action_key] += 1
                        self.betting_history['street_stats'][street]['total'] += 1
            
            # Update opponent stats
            if player_id != self.player_id:
                if player_id not in self.betting_history['opponent_stats']:
                    self.betting_history['opponent_stats'][player_id] = {
                        'hands_played': 0,
                        'raises': 0,
                        'calls': 0,
                        'folds': 0,
                        'vpip': 0,  # Voluntarily put in pot
                        'pfr': 0,   # Pre-flop raise
                        'total_actions': 0,
                        'aggression_factor': 0.0
                    }
                
                opp_stats = self.betting_history['opponent_stats'][player_id]
                
                # Track preflop actions for VPIP/PFR
                if street == 'preflop':
                    # Increment hands_played when opponent acts preflop (first action)
                    if opp_stats['total_actions'] == 0:
                        opp_stats['hands_played'] += 1
                    if action_type != 'fold':
                        opp_stats['vpip'] += 1
                    if action_type == 'raise':
                        opp_stats['pfr'] += 1
                
                # Update action counts
                if action_type == 'raise':
                    opp_stats['raises'] += 1
                elif action_type == 'call':
                    opp_stats['calls'] += 1
                elif action_type == 'fold':
                    opp_stats['folds'] += 1
                
                opp_stats['total_actions'] += 1
                
                # Calculate aggression factor: (raises) / (raises + calls)
                total_aggressive = opp_stats['raises'] + opp_stats['calls']
                if total_aggressive > 0:
                    opp_stats['aggression_factor'] = opp_stats['raises'] / total_aggressive
                else:
                    opp_stats['aggression_factor'] = 0.0
            
            # Add to recent actions (keep last 50)
            self.betting_history['recent_actions'].append(action_record)
            if len(self.betting_history['recent_actions']) > 50:
                self.betting_history['recent_actions'] = self.betting_history['recent_actions'][-50:]
                
        except Exception as e:
            # Log error for debugging but don't disrupt gameplay
            import traceback
            if hasattr(self, '_debug_betting_history') and self._debug_betting_history:
                print(f"Warning: Failed to record action for player {player_id}: {e}")
                traceback.print_exc()
    
    def get_opponent_stats(self, opponent_id: int) -> Dict[str, Any]:
        """Get betting statistics for a specific opponent."""
        if opponent_id in self.betting_history['opponent_stats']:
            stats = self.betting_history['opponent_stats'][opponent_id].copy()
            
            # Calculate frequencies
            total = stats['total_actions']
            if total > 0:
                stats['raise_frequency'] = stats['raises'] / total
                stats['call_frequency'] = stats['calls'] / total
                stats['fold_frequency'] = stats['folds'] / total
            else:
                stats['raise_frequency'] = 0.0
                stats['call_frequency'] = 0.0
                stats['fold_frequency'] = 0.0
            
            # VPIP/PFR percentages (need hands_played to be tracked)
            if stats.get('hands_played', 0) > 0:
                stats['vpip_pct'] = stats['vpip'] / stats['hands_played']
                stats['pfr_pct'] = stats['pfr'] / stats['hands_played']
            else:
                stats['vpip_pct'] = 0.0
                stats['pfr_pct'] = 0.0
            
            return stats
        else:
            # Return default stats for unknown opponent
            return {
                'raise_frequency': 0.33,
                'call_frequency': 0.33,
                'fold_frequency': 0.34,
                'aggression_factor': 0.5,
                'vpip_pct': 0.3,
                'pfr_pct': 0.1
            }
    
    def get_street_betting_stats(self, street: str) -> Dict[str, float]:
        """Get betting statistics for a specific street across all games."""
        if street in self.betting_history['street_stats']:
            stats = self.betting_history['street_stats'][street]
            total = stats['total']
            
            if total > 0:
                return {
                    'raise_frequency': stats['raises'] / total,
                    'call_frequency': stats['calls'] / total,
                    'fold_frequency': stats['folds'] / total,
                    'aggression_factor': stats['raises'] / max(stats['raises'] + stats['calls'], 1)
                }
        
        return {
            'raise_frequency': 0.33,
            'call_frequency': 0.33,
            'fold_frequency': 0.34,
            'aggression_factor': 0.5
        }

    def choose_action(self, state: pkrs.State) -> pkrs.Action:
        """
        Choose action using the appropriate decision tree.
        
        Args:
            state: Current poker state
            
        Returns:
            Chosen poker action
        """
        try:
            # Extract features with betting history
            features = extract_interpretable_features(state, self.player_id, self.betting_history)
            street = features['street']
            
            if street not in self.trees or self.trees[street] is None:
                # Fallback to random action if no tree available
                return self._get_random_action(state)
            
            # Convert to feature vector
            X = self._features_to_vector(features, tree=self.trees[street])
            
            # Predict action
            action_category = self.trees[street].predict([X])[0]
            
            # Convert to pokers action
            action = self._category_to_action(action_category, state, features)
            
            # Record decision for analysis
            self._record_decision(state, features, action_category, action)
            
            # Record action in betting history
            self.record_action(state, self.player_id, action)
            
            return action
            
        except Exception as e:
            print(f"Error in choose_action: {e}")
            return self._get_random_action(state)
    
    def _features_to_vector(self, features: Dict[str, Any], tree=None) -> np.ndarray:
        """Convert features dictionary to numpy vector.
        
        If tree is provided, only uses features that the tree was trained with.
        Otherwise, uses all features from self.feature_names.
        """
        vector = []
        
        # Determine which features to use
        if tree is not None:
            if hasattr(tree, 'feature_names_in_'):
                # New sklearn: tree has feature names
                feature_names_to_use = list(tree.feature_names_in_)
            elif hasattr(tree, 'n_features_'):
                # Older sklearn: use first N features where N = tree.n_features_
                num_features = tree.n_features_
                feature_names_to_use = self.feature_names[:num_features]
            elif hasattr(tree, 'tree_') and hasattr(tree.tree_, 'n_features'):
                # Fallback: use tree_.n_features
                num_features = tree.tree_.n_features
                feature_names_to_use = self.feature_names[:num_features]
            else:
                # No feature count info, use all features (shouldn't happen)
                feature_names_to_use = self.feature_names
        else:
            # Use all features (for compatibility)
            feature_names_to_use = self.feature_names
        
        for name in feature_names_to_use:
            if name in features:
                value = features[name]
                if isinstance(value, (int, float)):
                    vector.append(float(value))
                elif isinstance(value, str):
                    # Convert string categories to numeric
                    if name == 'position':
                        vector.append({'blinds': 0, 'early': 1, 'middle': 2, 'late': 3}.get(value, 0))
                    elif name == 'street':
                        vector.append({'preflop': 0, 'flop': 1, 'turn': 2, 'river': 3, 'showdown': 4}.get(value, 0))
                    else:
                        vector.append(0.0)
                else:
                    vector.append(0.0)
            else:
                vector.append(0.0)
        
        return np.array(vector, dtype=np.float32)
    
    def _category_to_action(self, action_category: str, state: pkrs.State, 
                           features: Dict[str, Any]) -> pkrs.Action:
        """Convert action category to pokers action."""
        if action_category == 'fold':
            return pkrs.Action(pkrs.ActionEnum.Fold)
        elif action_category == 'call':
            if state.min_bet == 0:
                return pkrs.Action(pkrs.ActionEnum.Check)
            else:
                return pkrs.Action(pkrs.ActionEnum.Call)
        elif action_category == 'raise':
            # Calculate bet size based on pot size and features
            bet_size = self._calculate_bet_size(state, features)
            return pkrs.Action(pkrs.ActionEnum.Raise, bet_size)
        else:
            # Default to fold
            return pkrs.Action(pkrs.ActionEnum.Fold)
    
    def _calculate_bet_size(self, state: pkrs.State, features: Dict[str, Any]) -> float:
        """Calculate bet size for raise actions."""
        # Simple bet sizing based on pot size and hand equity
        pot_size = state.pot
        hand_equity = features.get('hand_equity', 0.5)
        
        # Bet sizing: 0.5x to 2x pot based on hand strength
        if hand_equity > 0.8:
            bet_multiplier = 1.5  # Strong hand, big bet
        elif hand_equity > 0.6:
            bet_multiplier = 1.0  # Good hand, standard bet
        elif hand_equity > 0.4:
            bet_multiplier = 0.75  # Medium hand, smaller bet
        else:
            bet_multiplier = 0.5  # Weak hand, small bet
        
        bet_amount = pot_size * bet_multiplier
        
        # Ensure bet is at least the minimum
        min_bet = state.min_bet
        if bet_amount < min_bet:
            bet_amount = min_bet
        
        return bet_amount
    
    def _get_random_action(self, state: pkrs.State) -> pkrs.Action:
        """Fallback random action if tree prediction fails."""
        legal_actions = list(state.legal_actions)
        if not legal_actions:
            return pkrs.Action(pkrs.ActionEnum.Fold)
        
        # Choose random legal action
        import random
        action_enum = random.choice(legal_actions)
        
        if action_enum == pkrs.ActionEnum.Raise:
            bet_amount = state.min_bet + random.uniform(0, state.pot)
            return pkrs.Action(pkrs.ActionEnum.Raise, bet_amount)
        else:
            return pkrs.Action(action_enum)
    
    def explain_decision(self, state: pkrs.State) -> Dict[str, Any]:
        """
        Provide human-readable explanation of decision.
        
        Args:
            state: Current poker state
            
        Returns:
            Dictionary with decision explanation
        """
        try:
            features = extract_interpretable_features(state, self.player_id, self.betting_history)
            
            # Check if feature extraction failed
            if not features or len(features) == 0:
                return {
                    'action': 'fold',
                    'confidence': 0.0,
                    'explanation': 'Feature extraction failed - no features extracted',
                    'decision_path': [],
                    'features': {},
                    'probabilities': {'fold': 1.0, 'call': 0.0, 'raise': 0.0},
                    'recommended_bet_size': None
                }
            
            street = features.get('street', 'preflop')
            
            if street not in self.trees or self.trees[street] is None:
                return {
                    'action': 'fold',  # Default to fold if no tree available
                    'confidence': 0.0,
                    'explanation': f'No decision tree available for {street}',
                    'decision_path': [],
                    'features': features,
                    'probabilities': {'fold': 1.0, 'call': 0.0, 'raise': 0.0},
                    'recommended_bet_size': None
                }
            
            tree = self.trees[street]
            X = self._features_to_vector(features, tree=tree)
            
            # Validate feature vector length
            expected_features = tree.tree_.n_features if hasattr(tree, 'tree_') else len(self.feature_names)
            if len(X) != expected_features:
                return {
                    'action': 'fold',
                    'confidence': 0.0,
                    'explanation': f'Feature mismatch: got {len(X)} features, tree expects {expected_features}',
                    'decision_path': [],
                    'features': features,
                    'probabilities': {'fold': 1.0, 'call': 0.0, 'raise': 0.0},
                    'recommended_bet_size': None
                }
            
            # Get prediction and probability
            action_category = tree.predict([X])[0]
            action_proba = tree.predict_proba([X])[0]
            confidence = max(action_proba)
            
            # Get decision path
            decision_path = self._get_decision_path(tree, X, features)
            
            # Build explanation
            explanation = self._build_explanation(features, action_category, decision_path)
            
            # Build probabilities dictionary safely
            if hasattr(tree, 'classes_') and len(tree.classes_) == len(action_proba):
                probabilities = dict(zip(tree.classes_, action_proba))
            else:
                # Fallback if classes_ doesn't match
                probabilities = {'fold': 0.0, 'call': 0.0, 'raise': 0.0}
                if action_category in probabilities:
                    probabilities[action_category] = confidence
            
            # Calculate recommended bet size if action is raise
            recommended_bet_size = None
            if action_category == 'raise':
                recommended_bet_size = self._calculate_bet_size(state, features)
            
            return {
                'action': action_category,
                'confidence': confidence,
                'explanation': explanation,
                'decision_path': decision_path,
                'features': features,
                'probabilities': probabilities,
                'recommended_bet_size': recommended_bet_size
            }
            
        except Exception as e:
            return {
                'action': 'fold',  # Default to fold on error
                'confidence': 0.0,
                'explanation': f'Error generating explanation: {e}',
                'decision_path': [],
                'features': {},
                'probabilities': {'fold': 1.0, 'call': 0.0, 'raise': 0.0},
                'recommended_bet_size': None
            }
    
    def _get_decision_path(self, tree: DecisionTreeClassifier, X: np.ndarray, 
                          features: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get the decision path through the tree."""
        decision_path = []
        
        # Get decision path
        node_indicator = tree.decision_path([X])
        leaf_id = tree.apply([X])[0]
        
        # Get feature names - use self.feature_names instead of generic names
        # This ensures we always have proper feature names even if tree doesn't preserve them
        if hasattr(tree, 'feature_names_in_') and tree.feature_names_in_ is not None:
            feature_names = list(tree.feature_names_in_)
        else:
            # Use the feature names from get_feature_names() instead of generic names
            feature_names = self.feature_names
        
        # Traverse the path
        node_id = node_indicator.indices[node_indicator.indptr[0]:node_indicator.indptr[1]]
        
        for i, node in enumerate(node_id):
            if node == leaf_id:
                break
            
            # Get node information
            threshold = tree.tree_.threshold[node]
            feature_idx = tree.tree_.feature[node]
            
            if feature_idx >= 0 and feature_idx < len(feature_names):
                feature_name = feature_names[feature_idx]
                feature_value = X[feature_idx] if feature_idx < len(X) else 0
                
                decision_path.append({
                    'feature': feature_name,
                    'threshold': threshold,
                    'value': feature_value,
                    'condition': f"{feature_name} <= {threshold:.3f}" if feature_value <= threshold else f"{feature_name} > {threshold:.3f}"
                })
        
        return decision_path
    
    def _build_explanation(self, features: Dict[str, Any], action: str, 
                          decision_path: List[Dict[str, Any]]) -> str:
        """Build human-readable explanation of the decision."""
        explanations = []
        
        # Add key factors
        hand_equity = features.get('hand_equity', 0)
        pot_odds = features.get('pot_odds', 0)
        position = features.get('position', 'unknown')
        pot_size = features.get('pot_size_bb', 0)
        
        explanations.append(f"Hand equity: {hand_equity:.1%}")
        explanations.append(f"Pot odds: {pot_odds:.1%}")
        explanations.append(f"Position: {position}")
        explanations.append(f"Pot size: {pot_size:.1f} BB")
        
        # Add decision path
        if decision_path:
            explanations.append("Decision path:")
            for step in decision_path[:3]:  # Show first 3 conditions
                explanations.append(f"  - {step['condition']}")
        
        # Add final decision
        action_explanations = {
            'fold': "Fold due to weak hand or poor pot odds",
            'call': "Call to see the next card or for pot odds",
            'raise': "Raise for value or as a bluff"
        }
        
        explanations.append(f"Decision: {action.upper()} - {action_explanations.get(action, 'Unknown reason')}")
        
        return "\n".join(explanations)
    
    def _record_decision(self, state: pkrs.State, features: Dict[str, Any], 
                        action_category: str, action: pkrs.Action) -> None:
        """Record decision for analysis."""
        decision_record = {
            'street': features.get('street', 'unknown'),
            'action': action_category,
            'hand_equity': features.get('hand_equity', 0),
            'pot_odds': features.get('pot_odds', 0),
            'position': features.get('position', 'unknown'),
            'pot_size': features.get('pot_size_bb', 0),
            'stack_size': features.get('stack_size_bb', 0)
        }
        
        self.decision_history.append(decision_record)
        
        # Keep only recent history
        if len(self.decision_history) > 1000:
            self.decision_history = self.decision_history[-500:]
    
    def get_decision_history(self) -> pd.DataFrame:
        """Get decision history as DataFrame."""
        return pd.DataFrame(self.decision_history)
    
    def get_strategy_summary(self) -> Dict[str, Any]:
        """Get summary of agent's strategy."""
        if not self.decision_history:
            return {'message': 'No decisions recorded yet'}
        
        df = pd.DataFrame(self.decision_history)
        
        summary = {
            'total_decisions': len(df),
            'action_distribution': df['action'].value_counts().to_dict(),
            'street_distribution': df['street'].value_counts().to_dict(),
            'avg_hand_equity': df['hand_equity'].mean(),
            'avg_pot_odds': df['pot_odds'].mean(),
            'position_distribution': df['position'].value_counts().to_dict()
        }
        
        return summary

def create_interpretable_agent(player_id: int = 0, tree_dir: str = 'models/interpretable') -> InterpretablePokerAgent:
    """Convenience function to create an interpretable agent."""
    return InterpretablePokerAgent(player_id=player_id, tree_dir=tree_dir)

