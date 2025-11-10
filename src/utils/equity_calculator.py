"""
Monte Carlo equity calculator for poker hands.
Provides hand strength evaluation and equity distribution analysis.
"""

import random
import numpy as np
from typing import List, Tuple, Dict, Optional
import pokers as pkrs
from functools import lru_cache
import time

class EquityCalculator:
    """Monte Carlo equity calculator with caching for poker hands."""
    
    def __init__(self, cache_size=10000):
        self.cache_size = cache_size
        self.equity_cache = {}
        self.distribution_cache = {}
        
    def _get_hand_strength(self, hole_cards: List, community_cards: List) -> int:
        """Get hand strength using pokers library evaluation."""
        try:
            # Create a temporary state to evaluate hand strength
            # This is a simplified approach - in practice you'd need proper hand evaluation
            if len(hole_cards) == 2 and len(community_cards) >= 0:
                # Basic hand strength calculation
                # This is a placeholder - you'd implement proper hand ranking
                return self._basic_hand_strength(hole_cards, community_cards)
            return 0
        except Exception:
            return 0
    
    def _basic_hand_strength(self, hole_cards: List, community_cards: List) -> int:
        """Basic hand strength calculation (placeholder implementation)."""
        # This is a simplified version - in practice you'd use proper poker hand evaluation
        # For now, return a random strength for demonstration
        return random.randint(0, 1000)
    
    def calculate_equity(self, hole_cards: List, community_cards: List, 
                        num_opponents: int = 1, num_simulations: int = 1000) -> float:
        """
        Calculate win probability using Monte Carlo simulation.
        
        Args:
            hole_cards: List of hole cards
            community_cards: List of community cards (0-5 cards)
            num_opponents: Number of opponents to simulate against
            num_simulations: Number of Monte Carlo simulations
            
        Returns:
            Win probability (0.0 to 1.0)
        """
        # Create cache key
        cache_key = self._create_cache_key(hole_cards, community_cards, num_opponents)
        
        if cache_key in self.equity_cache:
            return self.equity_cache[cache_key]
        
        wins = 0
        total_simulations = 0
        
        for _ in range(num_simulations):
            try:
                # Simulate random opponent hands and board completion
                result = self._simulate_hand(hole_cards, community_cards, num_opponents)
                if result == 1:  # Win
                    wins += 1
                total_simulations += 1
            except Exception:
                # Skip invalid simulations
                continue
        
        if total_simulations == 0:
            equity = 0.0
        else:
            equity = wins / total_simulations
            
        # Cache result
        if len(self.equity_cache) < self.cache_size:
            self.equity_cache[cache_key] = equity
            
        return equity
    
    def calculate_equity_distribution(self, hole_cards: List, community_cards: List,
                                    num_opponents: int = 1, num_buckets: int = 10,
                                    num_simulations: int = 1000) -> List[float]:
        """
        Calculate equity distribution (histogram) for future board runouts.
        
        Args:
            hole_cards: List of hole cards
            community_cards: List of community cards (0-5 cards)
            num_opponents: Number of opponents to simulate against
            num_buckets: Number of histogram buckets (deciles)
            num_simulations: Number of Monte Carlo simulations
            
        Returns:
            List of equity values for each bucket
        """
        cache_key = f"dist_{self._create_cache_key(hole_cards, community_cards, num_opponents)}"
        
        if cache_key in self.distribution_cache:
            return self.distribution_cache[cache_key]
        
        equity_values = []
        
        for _ in range(num_simulations):
            try:
                equity = self._simulate_single_equity(hole_cards, community_cards, num_opponents)
                equity_values.append(equity)
            except Exception:
                continue
        
        if not equity_values:
            return [0.0] * num_buckets
        
        # Create histogram buckets
        equity_values.sort()
        bucket_size = len(equity_values) // num_buckets
        buckets = []
        
        for i in range(num_buckets):
            start_idx = i * bucket_size
            end_idx = (i + 1) * bucket_size if i < num_buckets - 1 else len(equity_values)
            if start_idx < len(equity_values):
                bucket_avg = np.mean(equity_values[start_idx:end_idx])
                buckets.append(bucket_avg)
            else:
                buckets.append(0.0)
        
        # Cache result
        if len(self.distribution_cache) < self.cache_size:
            self.distribution_cache[cache_key] = buckets
            
        return buckets
    
    def _create_cache_key(self, hole_cards: List, community_cards: List, num_opponents: int) -> str:
        """Create cache key for equity calculation."""
        hole_str = str(sorted([(int(card.rank), int(card.suit)) for card in hole_cards]))
        community_str = str(sorted([(int(card.rank), int(card.suit)) for card in community_cards]))
        return f"{hole_str}_{community_str}_{num_opponents}"
    
    def _simulate_hand(self, hole_cards: List, community_cards: List, num_opponents: int) -> int:
        """
        Simulate a single hand and return result.
        Returns: 1 for win, 0 for loss, -1 for tie
        """
        # This is a simplified simulation
        # In practice, you'd:
        # 1. Generate random opponent hands
        # 2. Complete the board with random cards
        # 3. Evaluate all hands
        # 4. Determine winner
        
        # For now, return random result
        return random.choice([-1, 0, 1])
    
    def _simulate_single_equity(self, hole_cards: List, community_cards: List, num_opponents: int) -> float:
        """Simulate a single equity calculation."""
        # Simplified equity calculation
        # In practice, you'd run a full Monte Carlo simulation
        return random.random()
    
    def get_equity_percentile(self, hole_cards: List, community_cards: List, 
                            num_opponents: int = 1, num_simulations: int = 1000) -> float:
        """
        Calculate equity percentile vs random hands.
        
        Returns:
            Percentile (0-100) of this hand vs random hands
        """
        # Get equity of current hand
        current_equity = self.calculate_equity(hole_cards, community_cards, num_opponents, num_simulations)
        
        # Compare against random hands
        random_equities = []
        for _ in range(100):  # Sample 100 random hands
            # Generate random hole cards (simplified)
            random_equity = random.random()  # Placeholder
            random_equities.append(random_equity)
        
        # Calculate percentile
        random_equities.sort()
        percentile = 0
        for i, equity in enumerate(random_equities):
            if current_equity >= equity:
                percentile = (i + 1) / len(random_equities) * 100
            else:
                break
                
        return percentile
    
    def clear_cache(self):
        """Clear all caches."""
        self.equity_cache.clear()
        self.distribution_cache.clear()
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics."""
        return {
            'equity_cache_size': len(self.equity_cache),
            'distribution_cache_size': len(self.distribution_cache),
            'total_cache_size': len(self.equity_cache) + len(self.distribution_cache)
        }

# Global equity calculator instance
_equity_calculator = None

def get_equity_calculator() -> EquityCalculator:
    """Get global equity calculator instance."""
    global _equity_calculator
    if _equity_calculator is None:
        _equity_calculator = EquityCalculator()
    return _equity_calculator

def calculate_equity(hole_cards: List, community_cards: List, 
                    num_opponents: int = 1, num_simulations: int = 1000) -> float:
    """Convenience function to calculate equity."""
    return get_equity_calculator().calculate_equity(hole_cards, community_cards, num_opponents, num_simulations)

def calculate_equity_distribution(hole_cards: List, community_cards: List,
                                num_opponents: int = 1, num_buckets: int = 10,
                                num_simulations: int = 1000) -> List[float]:
    """Convenience function to calculate equity distribution."""
    return get_equity_calculator().calculate_equity_distribution(
        hole_cards, community_cards, num_opponents, num_buckets, num_simulations
    )

def get_equity_percentile(hole_cards: List, community_cards: List,
                         num_opponents: int = 1, num_simulations: int = 1000) -> float:
    """Convenience function to get equity percentile."""
    return get_equity_calculator().get_equity_percentile(hole_cards, community_cards, num_opponents, num_simulations)

