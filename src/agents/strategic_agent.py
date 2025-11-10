"""
Strategic poker agent that follows calling ranges based on pot odds.
Uses hand range tables to determine calling strategy.
"""

import random
import pokers as pkrs
from typing import Dict, List, Tuple, Optional
from src.utils.settings import STRICT_CHECKING
from src.utils.logging import log_game_error

class StrategicAgent:
    """
    Strategic agent that follows calling ranges based on pot odds and tightness level.
    Uses hand range tables similar to professional poker strategy.
    """
    
    def __init__(self, player_id: int, tightness: str = 'average'):
        """
        Initialize strategic agent.
        
        Args:
            player_id: Player ID
            tightness: Strategy tightness level
                Options: 'very_tight' (3%), 'tight' (5%), 'average' (10%), 
                         'loose' (25%), 'very_loose' (50%), 'any_two' (100%)
        """
        self.player_id = player_id
        self.name = f"StrategicAgent_{player_id}_{tightness}"
        self.tightness = tightness
        
        # Load calling ranges based on tightness
        self.calling_ranges = self._load_calling_ranges()
    
    def _load_calling_ranges(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Load calling ranges from the strategy table.
        Returns dict mapping tightness -> pot_odds -> list of hands
        """
        ranges = {
            'very_tight': {
                '6_to_5': ['AA', 'KK', 'QQ'],
                '3_to_2': ['AA', 'KK', 'QQ', 'AKs'],
                '2_to_1': ['AA', 'KK', 'QQ', 'TT', 'AK']
            },
            'tight': {
                '6_to_5': ['AA', 'KK', 'QQ', 'JJ', 'AK'],
                '3_to_2': ['AA', 'KK', 'QQ', 'TT', 'AK'],
                '2_to_1': ['AA-22',  # All pairs
                          'AK', 'AQ', 'AJs', 'KJs', 'KTs', 'QJs', 'JTs']
            },
            'average': {
                '6_to_5': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', 'AK', 'AQ', 'AJs'],
                '3_to_2': ['AA-55',  # Pairs AA down to 55
                          'AK', 'AQ', 'AJ', 'ATs'],
                '2_to_1': ['AA-22',  # All pairs
                          'AK-AT',  # AK down to AT
                          'A9s-A2s',  # Suited aces
                          'KQ', 'KJs-K9s', 'QJs-Q9s', 'JTs-54s', 'J9s', 'J8s']
            },
            'loose': {
                '6_to_5': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44',
                          'AK', 'AQ', 'AJ', 'AT', 'A9', 'A8', 'A7s', 'KQ', 'KJs', 'KTs'],
                '3_to_2': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22',
                          'AK', 'AQ', 'AJ', 'AT', 'A9', 'A8', 'A7', 'A6', 'A5', 'A4', 'A3', 'A2',
                          'KQ', 'KJ', 'KT', 'K9s', 'K8s', 'K7s', 'K6s', 'QJ', 'QTs', 'Q9s', 'JTs'],
                '2_to_1': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22',
                          'AK', 'AQ', 'AJ', 'AT', 'A9', 'A8', 'A7', 'A6', 'A5', 'A4', 'A3', 'A2',
                          'KQ', 'KJ', 'KT', 'K9', 'K8', 'K7', 'K6', 'K5', 'K4', 'K3', 'K2',
                          'QJ', 'QT', 'Q9', 'Q8', 'Q7', 'Q6', 'Q5s', 'Q4s', 'Q3s', 'Q2s',
                          'JT', 'J9', 'J8', 'J7s', 'J6s', 'J5s', 'J4s', 'J3s', 'J2s',
                          'T9', 'T8', 'T7s', 'T6s', 'T5s', 'T4s', 'T3s',
                          '98', '97', '96s', '95s', '94s', '93s',
                          '87', '86', '85s', '84s',
                          '76', '75s', '74s', '73s',
                          '65', '64s', '63s',
                          '54s', '53s', '52s',
                          '43s', '42s']
            },
            'very_loose': {
                '6_to_5': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22',
                          'AK', 'AQ', 'AJ', 'AT', 'A9', 'A8', 'A7', 'A6', 'A5', 'A4', 'A3', 'A2',
                          'KQ', 'KJ', 'KT', 'K9', 'K8', 'K7', 'K6s', 'K5s', 'QJ', 'QT', 'Q9s', 'Q8s', 'JT', 'J9s'],
                '3_to_2': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22',
                          'AK', 'AQ', 'AJ', 'AT', 'A9', 'A8', 'A7', 'A6', 'A5', 'A4', 'A3', 'A2',
                          'KQ', 'KJ', 'KT', 'K9', 'K8', 'K7', 'K6', 'K5', 'K4', 'K3', 'K2',
                          'QJ', 'QT', 'Q9', 'Q8', 'Q7', 'Q6s', 'Q5s', 'Q4s', 'Q3s', 'Q2s',
                          'JT', 'J9', 'J8', 'J7s', 'J6s', 'T9', 'T8s', 'T7s', '98s'],
                '2_to_1': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22',
                          'AK', 'AQ', 'AJ', 'AT', 'A9', 'A8', 'A7', 'A6', 'A5', 'A4', 'A3', 'A2',
                          'KQ', 'KJ', 'KT', 'K9', 'K8', 'K7', 'K6', 'K5', 'K4', 'K3', 'K2',
                          'QJ', 'QT', 'Q9', 'Q8', 'Q7', 'Q6', 'Q5', 'Q4', 'Q3', 'Q2',
                          'JT', 'J9', 'J8', 'J7', 'J6', 'J5', 'J4', 'J3', 'J2',
                          'T9', 'T8', 'T7', 'T6', 'T5', 'T4', 'T3',
                          '98', '97', '96', '95',
                          '87', '86', '85',
                          '76', '75',
                          '65', '64',
                          '54', '53',
                          '43s', '42s', '32s']
            },
            'any_two': {
                '6_to_5': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22',
                          'AK', 'AQ', 'AJ', 'AT', 'A9', 'A8', 'A7', 'A6', 'A5', 'A4', 'A3', 'A2',
                          'KQ', 'KJ', 'KT', 'K9', 'K8', 'K7', 'K6', 'K5', 'K4', 'K3', 'K2',
                          'QJ', 'QT', 'Q9', 'Q8', 'Q7', 'Q6', 'Q5', 'Q4', 'Q3', 'Q2',
                          'JT', 'J9', 'J8', 'J7', 'J6', 'J5', 'J4', 'J3s', 'J2s',
                          'T9', 'T8', 'T7', 'T6s', 'T5s', 'T4s', 'T3s',
                          '98', '97', '96s', '95s',
                          '87s', '86s',
                          '76s', '75s',
                          '65s', '64s',
                          '54s'],
                '3_to_2': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22',
                          'AK', 'AQ', 'AJ', 'AT', 'A9', 'A8', 'A7', 'A6', 'A5', 'A4', 'A3', 'A2',
                          'KQ', 'KJ', 'KT', 'K9', 'K8', 'K7', 'K6', 'K5', 'K4', 'K3', 'K2',
                          'QJ', 'QT', 'Q9', 'Q8', 'Q7', 'Q6', 'Q5', 'Q4', 'Q3', 'Q2',
                          'JT', 'J9', 'J8', 'J7', 'J6', 'J5', 'J4', 'J3', 'J2',
                          'T9', 'T8', 'T7', 'T6', 'T5', 'T4', 'T3', 'T2',
                          '98', '97', '96', '95', '94s',
                          '87', '86', '85', '84s', '83s', '82s',
                          '76', '75', '74s', '73s',
                          '65s', '64s',
                          '54s'],
                '2_to_1': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22',
                          'AK', 'AQ', 'AJ', 'AT', 'A9', 'A8', 'A7', 'A6', 'A5', 'A4', 'A3', 'A2',
                          'KQ', 'KJ', 'KT', 'K9', 'K8', 'K7', 'K6', 'K5', 'K4', 'K3', 'K2',
                          'QJ', 'QT', 'Q9', 'Q8', 'Q7', 'Q6', 'Q5', 'Q4', 'Q3', 'Q2',
                          'JT', 'J9', 'J8', 'J7', 'J6', 'J5', 'J4', 'J3', 'J2',
                          'T9', 'T8', 'T7', 'T6', 'T5', 'T4', 'T3', 'T2',
                          '98', '97', '96', '95', '94', '93', '92',
                          '87', '86', '85', '84', '83', '82',
                          '76', '75', '74', '73', '72s',
                          '65', '64', '63', '62s',
                          '54', '53', '52s',
                          '43', '42s', '32s']
            }
        }
        
        return ranges.get(self.tightness, ranges['average'])
    
    def _card_to_notation(self, card: pkrs.Card) -> str:
        """Convert a card to notation (e.g., 'A', 'K', 'Q', '2')."""
        rank_map = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8', 
                   7: '9', 8: 'T', 9: 'J', 10: 'Q', 11: 'K', 12: 'A'}
        return rank_map.get(int(card.rank), str(int(card.rank)))
    
    def _hand_to_notation(self, hole_cards: List[pkrs.Card]) -> str:
        """
        Convert hole cards to poker notation (e.g., 'AA', 'AKs', 'KQo').
        
        Args:
            hole_cards: List of 2 hole cards
            
        Returns:
            Hand notation string (e.g., 'AA', 'AKs', 'KQ')
        """
        if len(hole_cards) != 2:
            return '22'  # Default fallback
        
        rank_map = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8', 
                   7: '9', 8: 'T', 9: 'J', 10: 'Q', 11: 'K', 12: 'A'}
        
        card1_rank = int(hole_cards[0].rank)
        card2_rank = int(hole_cards[1].rank)
        card1_suit = int(hole_cards[0].suit)
        card2_suit = int(hole_cards[1].suit)
        
        rank1_str = rank_map[card1_rank]
        rank2_str = rank_map[card2_rank]
        
        # Pair
        if card1_rank == card2_rank:
            return f"{rank1_str}{rank1_str}"
        
        # Suited or offsuit
        is_suited = (card1_suit == card2_suit)
        
        # High card first
        if card1_rank > card2_rank:
            if is_suited:
                return f"{rank1_str}{rank2_str}s"
            else:
                return f"{rank1_str}{rank2_str}"
        else:
            if is_suited:
                return f"{rank2_str}{rank1_str}s"
            else:
                return f"{rank2_str}{rank1_str}"
    
    def _hand_in_range(self, hand_notation: str, range_list: List[str]) -> bool:
        """
        Check if a hand notation matches any hand in a range list.
        
        Hand notation examples: 'AA', 'AKs', 'KQ', '22'
        Range can include: 'AA', 'AKs', 'AK', 'AA-22' (pairs range), 'AK-AQ' (unpaired range)
        """
        rank_map = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6,
                   '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
        
        # Normalize hand notation (handle both 'AK' and 'AKo')
        hand_is_pair = len(hand_notation) >= 2 and hand_notation[0] == hand_notation[1]
        hand_is_suited = hand_notation.endswith('s')
        hand_ranks = [hand_notation[0], hand_notation[1]] if len(hand_notation) >= 2 else []
        hand_high_rank = rank_map.get(hand_ranks[0], 0) if hand_ranks else 0
        hand_low_rank = rank_map.get(hand_ranks[1], 0) if hand_ranks else 0
        if hand_high_rank < hand_low_rank:
            hand_high_rank, hand_low_rank = hand_low_rank, hand_high_rank
        
        for range_hand in range_list:
            # Exact match
            if hand_notation == range_hand:
                return True
            
            # Handle ranges like 'AA-22' for pairs
            if '-' in range_hand:
                parts = range_hand.split('-')
                if len(parts) == 2:
                    start_hand = parts[0].strip()
                    end_hand = parts[1].strip()
                    
                    # Pair range (e.g., 'AA-22')
                    if len(start_hand) == 2 and len(end_hand) == 2 and start_hand[0] == start_hand[1]:
                        if hand_is_pair:
                            start_rank = rank_map.get(start_hand[0], 0)
                            end_rank = rank_map.get(end_hand[0], 0)
                            hand_rank = rank_map.get(hand_notation[0], 0)
                            # Check if hand rank is in range (handling both directions)
                            if min(start_rank, end_rank) <= hand_rank <= max(start_rank, end_rank):
                                return True
                    
                    # Unpaired range (e.g., 'AK-AQ', 'A9s-A2s')
                    elif len(start_hand) >= 2 and len(end_hand) >= 2:
                        # Handle suited ranges like 'A9s-A2s'
                        start_suited = start_hand.endswith('s')
                        end_suited = end_hand.endswith('s')
                        
                        # Remove 's' suffix for rank comparison
                        start_hand_clean = start_hand[:-1] if start_suited else start_hand
                        end_hand_clean = end_hand[:-1] if end_suited else end_hand
                        
                        start_high = rank_map.get(start_hand_clean[0], 0)
                        start_low = rank_map.get(start_hand_clean[1], 0) if len(start_hand_clean) >= 2 else 0
                        end_high = rank_map.get(end_hand_clean[0], 0)
                        end_low = rank_map.get(end_hand_clean[1], 0) if len(end_hand_clean) >= 2 else 0
                        
                        if not hand_is_pair:
                            # Check if high card matches and low card is in range
                            if start_high == end_high == hand_high_rank:
                                # Same high card (e.g., both A- hands or both K- hands)
                                if min(start_low, end_low) <= hand_low_rank <= max(start_low, end_low):
                                    # Check suited/offsuit
                                    if start_suited and end_suited:
                                        # Both suited in range, check if our hand is suited
                                        if hand_is_suited:
                                            return True
                                    elif not start_suited and not end_suited:
                                        # Both offsuit in range, check if our hand is offsuit
                                        if not hand_is_suited:
                                            return True
                                    else:
                                        # Mixed (shouldn't happen but handle it)
                                        return True
                            # Check cross-high-card ranges (e.g., 'AK-AQ' where both start with A)
                            elif start_high == hand_high_rank or end_high == hand_high_rank:
                                # For ranges like 'AK-AQ', check if hand matches either end
                                if (start_high == hand_high_rank and start_low == hand_low_rank):
                                    if (start_suited and hand_is_suited) or (not start_suited and not hand_is_suited):
                                        return True
                                if (end_high == hand_high_rank and end_low == hand_low_rank):
                                    if (end_suited and hand_is_suited) or (not end_suited and not hand_is_suited):
                                        return True
        
        return False
    
    def _calculate_pot_odds_category(self, state: pkrs.State) -> str:
        """
        Calculate pot odds and return category based on table.
        Returns: '6_to_5' (best pot odds), '3_to_2' (good), '2_to_1' (moderate), or 'worse'
        
        The table categories seem to represent increasingly favorable pot odds:
        - 6_to_5: Best pot odds (very favorable situations)
        - 3_to_2: Good pot odds (favorable situations)  
        - 2_to_1: Moderate pot odds (acceptable situations)
        """
        if state.pot == 0:
            return 'worse'
        
        call_amount = state.min_bet - state.players_state[state.current_player].bet_chips
        if call_amount <= 0:
            return 'worse'
        
        pot_odds_ratio = state.pot / call_amount
        
        # Categorize based on pot odds ratio
        # Higher ratio = better pot odds = more likely to call
        # Use thresholds that make sense for poker pot odds
        if pot_odds_ratio >= 10.0:  # Very favorable (pot is 10x+ the call)
            return '6_to_5'
        elif pot_odds_ratio >= 4.0:  # Good (pot is 4x+ the call)
            return '3_to_2'
        elif pot_odds_ratio >= 1.8:  # Moderate (pot is ~2x the call)
            return '2_to_1'
        else:
            return 'worse'
    
    def choose_action(self, state: pkrs.State) -> pkrs.Action:
        """
        Choose action based on calling ranges and pot odds.
        """
        if not state.legal_actions:
            print(f"WARNING: No legal actions available for player {self.player_id}")
            return pkrs.Action(pkrs.ActionEnum.Fold)
        
        # Get hole cards
        hole_cards = state.players_state[state.current_player].hand
        if len(hole_cards) != 2:
            # Fallback to random if we can't get cards
            return self._random_action(state)
        
        # Convert to notation
        hand_notation = self._hand_to_notation(hole_cards)
        
        # Calculate pot odds category
        pot_odds_category = self._calculate_pot_odds_category(state)
        
        # Check calling ranges - check all categories up to current pot odds
        # Better pot odds = can call with looser ranges
        categories_to_check = []
        if pot_odds_category == '6_to_5':
            categories_to_check = ['6_to_5', '3_to_2', '2_to_1']
        elif pot_odds_category == '3_to_2':
            categories_to_check = ['3_to_2', '2_to_1']
        elif pot_odds_category == '2_to_1':
            categories_to_check = ['2_to_1']
        
        hand_in_range = False
        for category in categories_to_check:
            if category in self.calling_ranges:
                range_list = self.calling_ranges[category]
                if self._hand_in_range(hand_notation, range_list):
                    hand_in_range = True
                    break
        
        # If hand is in calling range, prefer call/check
        if hand_in_range:
            if pkrs.ActionEnum.Check in state.legal_actions:
                return pkrs.Action(pkrs.ActionEnum.Check)
            elif pkrs.ActionEnum.Call in state.legal_actions:
                return pkrs.Action(pkrs.ActionEnum.Call)
            # Could also raise sometimes if in range, but for now just call/check
        
        # If hand not in range or pot odds are worse, fold if possible
        if pkrs.ActionEnum.Fold in state.legal_actions:
            # But sometimes call anyway (bluff/defense) with small probability
            if random.random() < 0.1:  # 10% chance to call anyway
                if pkrs.ActionEnum.Call in state.legal_actions:
                    return pkrs.Action(pkrs.ActionEnum.Call)
                elif pkrs.ActionEnum.Check in state.legal_actions:
                    return pkrs.Action(pkrs.ActionEnum.Check)
            return pkrs.Action(pkrs.ActionEnum.Fold)
        
        # Fallback to random action
        return self._random_action(state)
    
    def _random_action(self, state: pkrs.State) -> pkrs.Action:
        """Fallback random action."""
        legal_actions = list(state.legal_actions)
        if not legal_actions:
            return pkrs.Action(pkrs.ActionEnum.Fold)
        
        action_enum = random.choice(legal_actions)
        
        if action_enum == pkrs.ActionEnum.Raise:
            player_state = state.players_state[state.current_player]
            call_amount = max(0, state.min_bet - player_state.bet_chips)
            remaining_stake = player_state.stake - call_amount
            if remaining_stake > 0:
                bet_amount = min(state.min_bet + state.pot * 0.5, remaining_stake)
                return pkrs.Action(pkrs.ActionEnum.Raise, bet_amount)
            else:
                return pkrs.Action(pkrs.ActionEnum.Call)
        
        return pkrs.Action(action_enum)

