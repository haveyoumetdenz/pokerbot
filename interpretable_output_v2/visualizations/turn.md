# Turn Decision Tree Rules

## Overview
This document contains the decision rules learned by the interpretable poker AI for turn betting rounds.

## Feature Descriptions
| Feature | Description |
|---------|-------------|
| hand_equity | Probability of winning the hand (0-1) |
| equity_percentile | Percentile rank of hand strength vs random hands (0-100) |
| pot_size_bb | Pot size in big blinds |
| current_bet_bb | Current bet amount in big blinds |
| total_street_bets | Number of bets made this street |
| num_raises_this_street | Number of raises made this street |
| pot_odds | Pot odds for calling (0-1) |
| position_numeric | Position at table (0=blinds, 1=early, 2=middle, 3=late) |
| players_remaining | Number of active players |
| position_relative_button | Position relative to button (0-5) |
| stack_size_bb | Stack size in big blinds |
| effective_stack | Effective stack size (minimum among active players) |
| stack_to_pot_ratio | Ratio of stack size to pot size |
| street_numeric | Betting round (0=preflop, 1=flop, 2=turn, 3=river) |
| is_blind | Whether player is in small or big blind position |
| is_button | Whether player is on the button |
| players_to_act | Number of players who still need to act |
| has_been_raised | Whether there has been a raise this street |
| num_callers | Number of players who have called this street |
| aggression_factor | Measure of betting aggression this street |
| pot_commitment | Percentage of pot already committed by player |
| fold_equity | Estimated probability opponents will fold |


## Decision Rules

### Rule 1: RAISE
**Conditions:** effective_stack > 34.000 AND stack_to_pot_ratio > 0.382 AND stack_to_pot_ratio > 0.670 AND effective_stack > 40.649 AND stack_to_pot_ratio > 1.204 AND stack_to_pot_ratio > 2.036
**Samples:** 0
**Confidence:** 98.9%

### Rule 2: RAISE
**Conditions:** effective_stack > 34.000 AND stack_to_pot_ratio > 0.382 AND stack_to_pot_ratio > 0.670 AND effective_stack > 40.649 AND stack_to_pot_ratio > 1.204 AND stack_to_pot_ratio <= 2.036
**Samples:** 0
**Confidence:** 98.0%

### Rule 3: RAISE
**Conditions:** effective_stack > 34.000 AND stack_to_pot_ratio > 0.382 AND stack_to_pot_ratio <= 0.670 AND stack_size_bb <= 74.006 AND stack_size_bb > 52.550 AND pot_commitment > 0.162
**Samples:** 1
**Confidence:** 96.3%

### Rule 4: RAISE
**Conditions:** effective_stack > 34.000 AND stack_to_pot_ratio > 0.382 AND stack_to_pot_ratio > 0.670 AND effective_stack > 40.649 AND stack_to_pot_ratio <= 1.204 AND effective_stack > 43.000
**Samples:** 1
**Confidence:** 95.8%

### Rule 5: RAISE
**Conditions:** effective_stack > 34.000 AND stack_to_pot_ratio > 0.382 AND stack_to_pot_ratio > 0.670 AND effective_stack <= 40.649 AND pot_odds <= 0.286 AND current_bet_bb <= 21.949
**Samples:** 1
**Confidence:** 94.6%

### Rule 6: RAISE
**Conditions:** effective_stack > 34.000 AND stack_to_pot_ratio > 0.382 AND stack_to_pot_ratio <= 0.670 AND stack_size_bb > 74.006 AND effective_stack > 40.685 AND stack_size_bb <= 85.270
**Samples:** 1
**Confidence:** 94.5%

### Rule 7: FOLD
**Conditions:** effective_stack > 34.000 AND stack_to_pot_ratio > 0.382 AND stack_to_pot_ratio > 0.670 AND effective_stack <= 40.649 AND pot_odds > 0.286 AND pot_size_bb > 81.009
**Samples:** 0
**Confidence:** 92.7%

### Rule 8: FOLD
**Conditions:** effective_stack <= 34.000 AND effective_stack <= 4.500 AND pot_odds > 0.190 AND stack_size_bb > 69.047 AND pot_size_bb <= 128.659 AND players_to_act <= 1.500
**Samples:** 1
**Confidence:** 91.0%

### Rule 9: RAISE
**Conditions:** effective_stack <= 34.000 AND effective_stack > 4.500 AND stack_size_bb > 34.824 AND pot_odds > 0.163 AND pot_commitment > 0.285 AND effective_stack > 28.387
**Samples:** 0
**Confidence:** 90.2%

### Rule 10: RAISE
**Conditions:** effective_stack > 34.000 AND stack_to_pot_ratio > 0.382 AND stack_to_pot_ratio <= 0.670 AND stack_size_bb <= 74.006 AND stack_size_bb > 52.550 AND pot_commitment <= 0.162
**Samples:** 1
**Confidence:** 88.7%

### Rule 11: RAISE
**Conditions:** effective_stack <= 34.000 AND effective_stack > 4.500 AND stack_size_bb > 34.824 AND pot_odds <= 0.163 AND effective_stack > 22.361 AND stack_size_bb <= 54.930
**Samples:** 1
**Confidence:** 87.7%

### Rule 12: FOLD
**Conditions:** effective_stack > 34.000 AND stack_to_pot_ratio > 0.382 AND stack_to_pot_ratio <= 0.670 AND stack_size_bb > 74.006 AND effective_stack <= 40.685 AND effective_stack <= 37.740
**Samples:** 0
**Confidence:** 87.3%

### Rule 13: RAISE
**Conditions:** effective_stack > 34.000 AND stack_to_pot_ratio <= 0.382 AND stack_to_pot_ratio > 0.275 AND stack_size_bb > 49.944 AND stack_size_bb > 53.427 AND effective_stack <= 53.536
**Samples:** 1
**Confidence:** 87.0%

### Rule 14: FOLD
**Conditions:** effective_stack <= 34.000 AND effective_stack > 4.500 AND stack_size_bb > 34.824 AND pot_odds > 0.163 AND pot_commitment <= 0.285 AND stack_to_pot_ratio > 0.454
**Samples:** 1
**Confidence:** 86.4%

### Rule 15: FOLD
**Conditions:** effective_stack <= 34.000 AND effective_stack <= 4.500 AND pot_odds > 0.190 AND stack_size_bb > 69.047 AND pot_size_bb > 128.659 AND stack_size_bb > 78.513
**Samples:** 0
**Confidence:** 85.4%

### Rule 16: FOLD
**Conditions:** effective_stack <= 34.000 AND effective_stack <= 4.500 AND pot_odds > 0.190 AND stack_size_bb > 69.047 AND pot_size_bb <= 128.659 AND players_to_act > 1.500
**Samples:** 1
**Confidence:** 85.3%

### Rule 17: RAISE
**Conditions:** effective_stack > 34.000 AND stack_to_pot_ratio > 0.382 AND stack_to_pot_ratio > 0.670 AND effective_stack > 40.649 AND stack_to_pot_ratio <= 1.204 AND effective_stack <= 43.000
**Samples:** 1
**Confidence:** 85.3%

### Rule 18: CALL
**Conditions:** effective_stack <= 34.000 AND effective_stack <= 4.500 AND pot_odds <= 0.190 AND stack_to_pot_ratio > 0.021 AND stack_size_bb <= 32.360 AND pot_odds > 0.026
**Samples:** 0
**Confidence:** 82.9%

### Rule 19: RAISE
**Conditions:** effective_stack > 34.000 AND stack_to_pot_ratio > 0.382 AND stack_to_pot_ratio <= 0.670 AND stack_size_bb <= 74.006 AND stack_size_bb <= 52.550 AND stack_size_bb > 48.836
**Samples:** 0
**Confidence:** 82.4%

### Rule 20: FOLD
**Conditions:** effective_stack <= 34.000 AND effective_stack <= 4.500 AND pot_odds <= 0.190 AND stack_to_pot_ratio <= 0.021 AND effective_stack <= 0.535 AND stack_to_pot_ratio <= 0.014
**Samples:** 0
**Confidence:** 80.7%

## Feature Importance

| Feature | Importance |
|---------|------------|
| effective_stack | 0.864 |
| stack_to_pot_ratio | 0.054 |
| pot_odds | 0.048 |
| stack_size_bb | 0.028 |
| pot_size_bb | 0.005 |
| pot_commitment | 0.001 |
| current_bet_bb | 0.000 |
| position_relative_button | 0.000 |
| fold_equity | 0.000 |
| players_to_act | 0.000 |
