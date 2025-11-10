# River Decision Tree Rules

## Overview
This document contains the decision rules learned by the interpretable poker AI for river betting rounds.

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

### Rule 1: FOLD
**Conditions:** effective_stack <= 5.924 AND pot_odds <= 0.189 AND stack_to_pot_ratio <= 0.022 AND effective_stack <= 0.499 AND stack_to_pot_ratio <= 0.013 AND pot_size_bb > 413.824
**Samples:** 0
**Confidence:** 99.1%

### Rule 2: RAISE
**Conditions:** effective_stack > 5.924 AND effective_stack > 37.737 AND stack_size_bb > 51.064 AND stack_size_bb > 64.105 AND effective_stack > 40.571 AND stack_size_bb > 74.267
**Samples:** 0
**Confidence:** 98.0%

### Rule 3: RAISE
**Conditions:** effective_stack > 5.924 AND effective_stack > 37.737 AND stack_size_bb > 51.064 AND stack_size_bb > 64.105 AND effective_stack <= 40.571 AND stack_size_bb <= 79.199
**Samples:** 1
**Confidence:** 96.0%

### Rule 4: RAISE
**Conditions:** effective_stack > 5.924 AND effective_stack > 37.737 AND stack_size_bb > 51.064 AND stack_size_bb > 64.105 AND effective_stack > 40.571 AND stack_size_bb <= 74.267
**Samples:** 1
**Confidence:** 95.3%

### Rule 5: RAISE
**Conditions:** effective_stack > 5.924 AND effective_stack > 37.737 AND stack_size_bb > 51.064 AND stack_size_bb <= 64.105 AND stack_size_bb > 56.749 AND stack_to_pot_ratio > 0.468
**Samples:** 1
**Confidence:** 92.5%

### Rule 6: RAISE
**Conditions:** effective_stack > 5.924 AND effective_stack <= 37.737 AND has_been_raised > 0.500 AND pot_odds <= 0.198 AND effective_stack > 22.594 AND effective_stack > 28.375
**Samples:** 0
**Confidence:** 92.3%

### Rule 7: FOLD
**Conditions:** effective_stack <= 5.924 AND pot_odds > 0.189 AND effective_stack <= 0.535 AND pot_size_bb <= 240.915 AND stack_size_bb > 65.822 AND stack_to_pot_ratio > 0.628
**Samples:** 1
**Confidence:** 90.9%

### Rule 8: FOLD
**Conditions:** effective_stack > 5.924 AND effective_stack <= 37.737 AND has_been_raised > 0.500 AND pot_odds > 0.198 AND effective_stack > 34.359 AND stack_size_bb > 73.863
**Samples:** 0
**Confidence:** 90.4%

### Rule 9: RAISE
**Conditions:** effective_stack > 5.924 AND effective_stack > 37.737 AND stack_size_bb <= 51.064 AND stack_to_pot_ratio > 0.345 AND stack_size_bb > 47.643 AND is_button > 0.500
**Samples:** 0
**Confidence:** 89.8%

### Rule 10: RAISE
**Conditions:** effective_stack > 5.924 AND effective_stack > 37.737 AND stack_size_bb > 51.064 AND stack_size_bb <= 64.105 AND stack_size_bb > 56.749 AND stack_to_pot_ratio <= 0.468
**Samples:** 0
**Confidence:** 89.0%

### Rule 11: RAISE
**Conditions:** effective_stack > 5.924 AND effective_stack > 37.737 AND stack_size_bb > 51.064 AND stack_size_bb <= 64.105 AND stack_size_bb <= 56.749 AND stack_to_pot_ratio > 0.362
**Samples:** 0
**Confidence:** 88.4%

### Rule 12: CALL
**Conditions:** effective_stack <= 5.924 AND pot_odds <= 0.189 AND stack_to_pot_ratio > 0.022 AND stack_size_bb <= 29.390 AND pot_odds > 0.026 AND stack_size_bb <= 19.753
**Samples:** 1
**Confidence:** 86.4%

### Rule 13: RAISE
**Conditions:** effective_stack > 5.924 AND effective_stack <= 37.737 AND has_been_raised > 0.500 AND pot_odds > 0.198 AND effective_stack > 34.359 AND stack_size_bb <= 73.863
**Samples:** 0
**Confidence:** 86.4%

### Rule 14: FOLD
**Conditions:** effective_stack > 5.924 AND effective_stack > 37.737 AND stack_size_bb > 51.064 AND stack_size_bb > 64.105 AND effective_stack <= 40.571 AND stack_size_bb > 79.199
**Samples:** 0
**Confidence:** 86.3%

### Rule 15: FOLD
**Conditions:** effective_stack > 5.924 AND effective_stack <= 37.737 AND has_been_raised > 0.500 AND pot_odds > 0.198 AND effective_stack <= 34.359 AND stack_size_bb > 61.134
**Samples:** 1
**Confidence:** 86.3%

### Rule 16: FOLD
**Conditions:** effective_stack <= 5.924 AND pot_odds > 0.189 AND effective_stack <= 0.535 AND pot_size_bb <= 240.915 AND stack_size_bb > 65.822 AND stack_to_pot_ratio <= 0.628
**Samples:** 1
**Confidence:** 84.5%

### Rule 17: RAISE
**Conditions:** effective_stack > 5.924 AND effective_stack > 37.737 AND stack_size_bb <= 51.064 AND stack_to_pot_ratio > 0.345 AND stack_size_bb > 47.643 AND is_button <= 0.500
**Samples:** 1
**Confidence:** 83.8%

### Rule 18: RAISE
**Conditions:** effective_stack > 5.924 AND effective_stack > 37.737 AND stack_size_bb > 51.064 AND stack_size_bb <= 64.105 AND stack_size_bb <= 56.749 AND stack_to_pot_ratio <= 0.362
**Samples:** 1
**Confidence:** 83.8%

### Rule 19: CALL
**Conditions:** effective_stack <= 5.924 AND pot_odds <= 0.189 AND stack_to_pot_ratio > 0.022 AND stack_size_bb <= 29.390 AND pot_odds > 0.026 AND stack_size_bb > 19.753
**Samples:** 0
**Confidence:** 80.0%

### Rule 20: RAISE
**Conditions:** effective_stack > 5.924 AND effective_stack > 37.737 AND stack_size_bb <= 51.064 AND stack_to_pot_ratio > 0.345 AND stack_size_bb <= 47.643 AND position_numeric > 0.500
**Samples:** 1
**Confidence:** 79.9%

## Feature Importance

| Feature | Importance |
|---------|------------|
| effective_stack | 0.899 |
| pot_odds | 0.039 |
| stack_size_bb | 0.022 |
| has_been_raised | 0.015 |
| stack_to_pot_ratio | 0.013 |
| pot_size_bb | 0.008 |
| position_relative_button | 0.003 |
| current_bet_bb | 0.000 |
| position_numeric | 0.000 |
| is_button | 0.000 |
