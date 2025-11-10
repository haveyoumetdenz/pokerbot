# Interpretable Poker AI Performance Report
==================================================

## Performance vs Random Opponents
- Average profit per game: 242.45
- Total profit: 121227.12
- Win rate: 62.4%
- Average decision time: 0.0004s
- Action distribution: {'fold': 123, 'call': 704, 'raise': 753}

## Decision Accuracy vs CFR Ground Truth
- preflop: 0.540 (54/100)
- flop: 0.330 (33/100)
- turn: 0.260 (26/100)
- river: 0.230 (23/100)

## Interpretability Metrics
- Total decisions analyzed: 978
- Action distribution: {'raise': 667, 'call': 274, 'fold': 37}
- Average hand equity: 0.334
- Average pot odds: 0.490

## Tree Complexity
- preflop: depth=8, leaves=227
- flop: depth=8, leaves=249
- turn: depth=6, leaves=64
- river: depth=6, leaves=64
