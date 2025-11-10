# Interpretable Poker AI Performance Report
==================================================

## Performance vs Random Opponents
- Average profit per game: 93.57
- Total profit: 46784.02
- Win rate: 22.6%
- Average decision time: 0.0004s
- Action distribution: {'fold': 370, 'call': 275, 'raise': 351}

## Decision Accuracy vs CFR Ground Truth
- preflop: 0.840 (84/100)
- flop: 0.290 (29/100)
- turn: 0.320 (32/100)
- river: 0.210 (21/100)

## Interpretability Metrics
- Total decisions analyzed: 895
- Action distribution: {'fold': 569, 'raise': 175, 'call': 151}
- Average hand equity: 0.335
- Average pot odds: 0.447

## Tree Complexity
- preflop: depth=12, leaves=2509
- flop: depth=12, leaves=2531
- turn: depth=6, leaves=64
- river: depth=12, leaves=2417
