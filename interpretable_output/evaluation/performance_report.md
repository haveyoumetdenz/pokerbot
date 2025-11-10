# Interpretable Poker AI Performance Report
==================================================

## Performance vs Random Opponents
- Average profit per game: 210.53
- Total profit: 105263.28
- Win rate: 61.6%
- Average decision time: 0.0002s
- Action distribution: {'fold': 122, 'call': 1217, 'raise': 512}

## Decision Accuracy vs CFR Ground Truth
- preflop: 0.310 (31/100)
- flop: 0.330 (33/100)
- turn: 0.300 (30/100)
- river: 0.320 (32/100)

## Interpretability Metrics
- Total decisions analyzed: 748
- Action distribution: {'raise': 387, 'call': 336, 'fold': 25}
- Average hand equity: 0.338
- Average pot odds: 0.465

## Tree Complexity
- preflop: depth=22, leaves=6524
- flop: depth=22, leaves=10801
- turn: depth=22, leaves=15017
- river: depth=22, leaves=13083
