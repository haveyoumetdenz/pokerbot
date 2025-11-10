"""
Interpretable feature extraction for poker decision trees.
Replaces the 500-dimensional neural network input with ~15-25 interpretable features.
"""

import numpy as np
import pokers as pkrs
from typing import Dict, List, Any, Optional
from src.utils.equity_calculator import get_equity_calculator, calculate_equity, get_equity_percentile

def extract_interpretable_features(state: pkrs.State, player_id: int, betting_history: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Extract interpretable features for decision tree input.
    
    Args:
        state: Current poker state
        player_id: ID of the player to extract features for
        betting_history: Optional betting history dictionary from InterpretablePokerAgent
        
    Returns:
        Dictionary with human-readable feature names and values
    """
    features = {}
    
    # Get basic game info
    num_players = len(state.players_state)
    big_blind = 2.0  # Assuming standard 1/2 blinds
    small_blind = 1.0
    
    # Hand strength features
    hole_cards = state.players_state[player_id].hand
    community_cards = state.public_cards
    
    # Calculate equity (simplified for now)
    equity_calc = get_equity_calculator()
    features['hand_equity'] = calculate_equity(hole_cards, community_cards, num_opponents=1, num_simulations=100)
    features['equity_percentile'] = get_equity_percentile(hole_cards, community_cards, num_opponents=1, num_simulations=100)
    
    # Betting history features
    features['pot_size_bb'] = state.pot / big_blind
    features['current_bet_bb'] = state.players_state[player_id].bet_chips / big_blind
    features['total_street_bets'] = _count_bets_this_street(state)
    features['num_raises_this_street'] = _count_raises_this_street(state)
    features['pot_odds'] = _calculate_pot_odds(state, player_id)
    
    # Position features
    features['position'] = _get_position_category(state, player_id)
    features['players_remaining'] = _count_active_players(state)
    features['position_relative_button'] = (player_id - state.button) % num_players
    
    # Stack features
    features['stack_size_bb'] = state.players_state[player_id].stake / big_blind
    features['effective_stack'] = _get_effective_stack(state, player_id) / big_blind
    features['stack_to_pot_ratio'] = features['stack_size_bb'] / max(features['pot_size_bb'], 0.1)
    
    # Street features
    street_names = ['preflop', 'flop', 'turn', 'river', 'showdown']
    features['street'] = street_names[int(state.stage)]
    features['street_numeric'] = int(state.stage)
    
    # Advanced features
    features['is_blind'] = player_id in [state.button, (state.button + 1) % num_players]
    features['is_button'] = player_id == state.button
    features['players_to_act'] = _count_players_to_act(state, player_id)
    
    # Betting pattern features
    features['has_been_raised'] = _has_been_raised_this_street(state)
    features['num_callers'] = _count_callers_this_street(state)
    features['aggression_factor'] = _calculate_aggression_factor(state)
    
    # Pot commitment features
    features['pot_commitment'] = _calculate_pot_commitment(state, player_id)
    features['fold_equity'] = _estimate_fold_equity(state, player_id)
    
    # Convert categorical features to numeric for decision trees
    features['position_numeric'] = _position_to_numeric(features['position'])
    features['street_numeric'] = int(state.stage)
    
    # Betting history features (if available)
    if betting_history is not None:
        current_street = features['street']
        
        # Street-level betting statistics
        street_stats = betting_history.get('street_stats', {})
        if current_street in street_stats:
            street_data = street_stats[current_street]
            total = street_data.get('total', 0)
            if total > 0:
                features['street_raise_frequency'] = street_data.get('raises', 0) / total
                features['street_call_frequency'] = street_data.get('calls', 0) / total
                features['street_fold_frequency'] = street_data.get('folds', 0) / total
                features['street_aggression_factor'] = street_data.get('raises', 0) / max(street_data.get('raises', 0) + street_data.get('calls', 0), 1)
            else:
                features['street_raise_frequency'] = 0.33
                features['street_call_frequency'] = 0.33
                features['street_fold_frequency'] = 0.34
                features['street_aggression_factor'] = 0.5
        else:
            features['street_raise_frequency'] = 0.33
            features['street_call_frequency'] = 0.33
            features['street_fold_frequency'] = 0.34
            features['street_aggression_factor'] = 0.5
        
        # Average opponent statistics
        opponent_stats = betting_history.get('opponent_stats', {})
        if opponent_stats:
            # Get average stats across all opponents
            avg_raise_freq = 0.0
            avg_call_freq = 0.0
            avg_fold_freq = 0.0
            avg_aggression = 0.0
            avg_vpip = 0.0
            avg_pfr = 0.0
            count = 0
            
            for opp_id, stats in opponent_stats.items():
                if opp_id != player_id:
                    total_actions = stats.get('total_actions', 0)
                    if total_actions > 0:
                        avg_raise_freq += stats.get('raises', 0) / total_actions
                        avg_call_freq += stats.get('calls', 0) / total_actions
                        avg_fold_freq += stats.get('folds', 0) / total_actions
                        avg_aggression += stats.get('aggression_factor', 0.0)
                        count += 1
                    
                    hands_played = stats.get('hands_played', 0)
                    if hands_played > 0:
                        avg_vpip += stats.get('vpip', 0) / hands_played
                        avg_pfr += stats.get('pfr', 0) / hands_played
            
            if count > 0:
                features['avg_opponent_raise_frequency'] = avg_raise_freq / count
                features['avg_opponent_call_frequency'] = avg_call_freq / count
                features['avg_opponent_fold_frequency'] = avg_fold_freq / count
                features['avg_opponent_aggression'] = avg_aggression / count
                features['avg_opponent_vpip'] = avg_vpip / count
                features['avg_opponent_pfr'] = avg_pfr / count
            else:
                features['avg_opponent_raise_frequency'] = 0.33
                features['avg_opponent_call_frequency'] = 0.33
                features['avg_opponent_fold_frequency'] = 0.34
                features['avg_opponent_aggression'] = 0.5
                features['avg_opponent_vpip'] = 0.3
                features['avg_opponent_pfr'] = 0.1
        else:
            features['avg_opponent_raise_frequency'] = 0.33
            features['avg_opponent_call_frequency'] = 0.33
            features['avg_opponent_fold_frequency'] = 0.34
            features['avg_opponent_aggression'] = 0.5
            features['avg_opponent_vpip'] = 0.3
            features['avg_opponent_pfr'] = 0.1
        
        # Game count (how many games have been played)
        features['games_played'] = betting_history.get('game_count', 0)
    else:
        # Default values when no betting history
        features['street_raise_frequency'] = 0.33
        features['street_call_frequency'] = 0.33
        features['street_fold_frequency'] = 0.34
        features['street_aggression_factor'] = 0.5
        features['avg_opponent_raise_frequency'] = 0.33
        features['avg_opponent_call_frequency'] = 0.33
        features['avg_opponent_fold_frequency'] = 0.34
        features['avg_opponent_aggression'] = 0.5
        features['avg_opponent_vpip'] = 0.3
        features['avg_opponent_pfr'] = 0.1
        features['games_played'] = 0
    
    return features

def get_feature_names() -> List[str]:
    """Get list of all feature names for decision tree training."""
    return [
        'hand_equity',
        'equity_percentile', 
        'pot_size_bb',
        'current_bet_bb',
        'total_street_bets',
        'num_raises_this_street',
        'pot_odds',
        'position',
        'players_remaining',
        'position_relative_button',
        'stack_size_bb',
        'effective_stack',
        'stack_to_pot_ratio',
        'street',
        'street_numeric',
        'is_blind',
        'is_button',
        'players_to_act',
        'has_been_raised',
        'num_callers',
        'aggression_factor',
        'pot_commitment',
        'fold_equity',
        'position_numeric',
        # Betting history features
        'street_raise_frequency',
        'street_call_frequency',
        'street_fold_frequency',
        'street_aggression_factor',
        'avg_opponent_raise_frequency',
        'avg_opponent_call_frequency',
        'avg_opponent_fold_frequency',
        'avg_opponent_aggression',
        'avg_opponent_vpip',
        'avg_opponent_pfr',
        'games_played'
    ]

def features_to_vector(features: Dict[str, Any]) -> np.ndarray:
    """Convert features dictionary to numpy vector for decision tree training."""
    feature_names = get_feature_names()
    vector = []
    
    for name in feature_names:
        if name in features:
            value = features[name]
            
            # Handle categorical features
            if name == 'position':
                # Convert position to numeric
                position_map = {'early': 0, 'middle': 1, 'late': 2, 'blinds': 3}
                vector.append(position_map.get(value, 0))
            elif name == 'street':
                # Convert street to numeric
                street_map = {'preflop': 0, 'flop': 1, 'turn': 2, 'river': 3}
                vector.append(street_map.get(value, 0))
            else:
                # Convert to float, handling any type issues
                try:
                    vector.append(float(value))
                except (ValueError, TypeError):
                    vector.append(0.0)
        else:
            vector.append(0.0)  # Default value for missing features
    
    return np.array(vector, dtype=np.float32)

def _count_bets_this_street(state: pkrs.State) -> int:
    """Count total bets made this street."""
    # Simplified implementation
    return len([p for p in state.players_state if p.bet_chips > 0])

def _count_raises_this_street(state: pkrs.State) -> int:
    """Count raises made this street."""
    # Simplified implementation - would need to track action history
    return 0

def _calculate_pot_odds(state: pkrs.State, player_id: int) -> float:
    """Calculate pot odds for the current player."""
    if state.pot == 0:
        return 0.0
    
    call_amount = state.min_bet - state.players_state[player_id].bet_chips
    if call_amount <= 0:
        return 1.0
    
    return call_amount / (call_amount + state.pot)

def _get_position_category(state: pkrs.State, player_id: int) -> str:
    """Get position category for the player."""
    num_players = len(state.players_state)
    relative_pos = (player_id - state.button) % num_players
    
    if relative_pos <= 1:
        return 'blinds'
    elif relative_pos <= 3:
        return 'early'
    elif relative_pos <= 5:
        return 'middle'
    else:
        return 'late'

def _position_to_numeric(position: str) -> int:
    """Convert position category to numeric value."""
    position_map = {'blinds': 0, 'early': 1, 'middle': 2, 'late': 3}
    return position_map.get(position, 0)

def _count_active_players(state: pkrs.State) -> int:
    """Count number of active players."""
    return sum(1 for p in state.players_state if p.active)

def _get_effective_stack(state: pkrs.State, player_id: int) -> float:
    """Get effective stack size (minimum stack among active players)."""
    active_stacks = [p.stake for p in state.players_state if p.active]
    if not active_stacks:
        return state.players_state[player_id].stake
    return min(active_stacks)

def _count_players_to_act(state: pkrs.State, player_id: int) -> int:
    """Count players who still need to act."""
    # Simplified - would need to track action order
    return _count_active_players(state) - 1

def _has_been_raised_this_street(state: pkrs.State) -> bool:
    """Check if there has been a raise this street."""
    # Simplified implementation
    return state.min_bet > 2.0  # Assuming big blind is 2

def _count_callers_this_street(state: pkrs.State) -> int:
    """Count players who have called this street."""
    # Simplified implementation
    return 0

def _calculate_aggression_factor(state: pkrs.State) -> float:
    """Calculate aggression factor for the current street."""
    # Simplified implementation
    return 0.0

def _calculate_pot_commitment(state: pkrs.State, player_id: int) -> float:
    """Calculate pot commitment percentage."""
    player_bet = state.players_state[player_id].bet_chips
    if state.pot == 0:
        return 0.0
    return player_bet / state.pot

def _estimate_fold_equity(state: pkrs.State, player_id: int) -> float:
    """Estimate fold equity based on position and betting history."""
    # Simplified implementation
    position = _get_position_category(state, player_id)
    if position == 'late':
        return 0.3  # Higher fold equity in late position
    elif position == 'early':
        return 0.1  # Lower fold equity in early position
    else:
        return 0.2  # Medium fold equity
