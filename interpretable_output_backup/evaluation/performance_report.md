# Interpretable Poker AI Performance Report
==================================================

## Performance vs Random Opponents
- Average profit per game: -75.49
- Total profit: -7549.38
- Win rate: 18.0%
- Average decision time: 0.0002s
- Action distribution: {'fold': 67, 'call': 66, 'raise': 145}

## Decision Accuracy vs CFR Ground Truth
- preflop: 0.610 (61/100)
- flop: 0.400 (40/100)
- turn: 0.220 (22/100)
- river: 0.260 (26/100)

## Interpretability Metrics
- Total decisions analyzed: 678
- Action distribution: {'raise': 545, 'fold': 67, 'call': 66}
- Average hand equity: 0.334
- Average pot odds: 0.432

## Tree Complexity
- preflop: depth=6, leaves=54
- flop: depth=8, leaves=194
- turn: depth=10, leaves=352
- river: depth=4, leaves=16
