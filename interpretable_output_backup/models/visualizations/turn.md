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

### Rule 1: FOLD
**Conditions:** stack_to_pot_ratio <= 0.119 AND pot_size_bb > 213.215 AND stack_to_pot_ratio <= 0.083 AND stack_to_pot_ratio <= 0.065 AND pot_size_bb > 219.500 AND stack_to_pot_ratio <= 0.054
**Samples:** 0
**Confidence:** 99.9%

### Rule 2: FOLD
**Conditions:** stack_to_pot_ratio <= 0.119 AND pot_size_bb > 213.215 AND stack_to_pot_ratio <= 0.083 AND stack_to_pot_ratio > 0.065 AND pot_size_bb > 293.441 AND effective_stack > 1.034
**Samples:** 0
**Confidence:** 99.3%

### Rule 3: CALL
**Conditions:** stack_to_pot_ratio > 0.119 AND effective_stack > 72.957 AND is_blind > 0.500 AND pot_odds <= 0.688 AND players_remaining > 2.500 AND pot_size_bb > 65.933
**Samples:** 1
**Confidence:** 98.1%

### Rule 4: FOLD
**Conditions:** stack_to_pot_ratio <= 0.119 AND pot_size_bb > 213.215 AND stack_to_pot_ratio <= 0.083 AND stack_to_pot_ratio <= 0.065 AND pot_size_bb > 219.500 AND stack_to_pot_ratio > 0.054
**Samples:** 1
**Confidence:** 96.7%

### Rule 5: FOLD
**Conditions:** stack_to_pot_ratio <= 0.119 AND pot_size_bb > 213.215 AND stack_to_pot_ratio > 0.083 AND pot_size_bb > 283.077 AND effective_stack > 13.589 AND pot_size_bb > 293.792
**Samples:** 0
**Confidence:** 95.8%

### Rule 6: FOLD
**Conditions:** stack_to_pot_ratio <= 0.119 AND pot_size_bb > 213.215 AND stack_to_pot_ratio <= 0.083 AND stack_to_pot_ratio > 0.065 AND pot_size_bb > 293.441 AND effective_stack <= 1.034
**Samples:** 0
**Confidence:** 95.5%

### Rule 7: CALL
**Conditions:** stack_to_pot_ratio > 0.119 AND effective_stack <= 72.957 AND effective_stack <= 43.989 AND stack_to_pot_ratio > 0.214 AND has_been_raised > 0.500 AND effective_stack <= 36.796
**Samples:** 0
**Confidence:** 93.6%

### Rule 8: FOLD
**Conditions:** stack_to_pot_ratio <= 0.119 AND pot_size_bb > 213.215 AND stack_to_pot_ratio <= 0.083 AND stack_to_pot_ratio <= 0.065 AND pot_size_bb <= 219.500 AND pot_size_bb > 215.038
**Samples:** 0
**Confidence:** 93.3%

### Rule 9: FOLD
**Conditions:** stack_to_pot_ratio <= 0.119 AND pot_size_bb <= 213.215 AND stack_to_pot_ratio <= 0.059 AND pot_size_bb > 198.040 AND position_relative_button > 4.500 AND pot_size_bb > 201.019
**Samples:** 0
**Confidence:** 91.2%

### Rule 10: CALL
**Conditions:** stack_to_pot_ratio > 0.119 AND effective_stack > 72.957 AND is_blind > 0.500 AND pot_odds <= 0.688 AND players_remaining <= 2.500 AND effective_stack <= 97.875
**Samples:** 0
**Confidence:** 89.7%

### Rule 11: FOLD
**Conditions:** stack_to_pot_ratio <= 0.119 AND pot_size_bb > 213.215 AND stack_to_pot_ratio <= 0.083 AND stack_to_pot_ratio > 0.065 AND pot_size_bb <= 293.441 AND effective_stack > 14.597
**Samples:** 0
**Confidence:** 88.2%

### Rule 12: CALL
**Conditions:** stack_to_pot_ratio > 0.119 AND effective_stack <= 72.957 AND effective_stack > 43.989 AND is_blind > 0.500 AND stack_size_bb <= 86.915 AND effective_stack <= 72.342
**Samples:** 1
**Confidence:** 88.0%

### Rule 13: FOLD
**Conditions:** stack_to_pot_ratio <= 0.119 AND pot_size_bb > 213.215 AND stack_to_pot_ratio <= 0.083 AND stack_to_pot_ratio <= 0.065 AND pot_size_bb <= 219.500 AND pot_size_bb <= 215.038
**Samples:** 0
**Confidence:** 88.0%

### Rule 14: FOLD
**Conditions:** stack_to_pot_ratio <= 0.119 AND pot_size_bb > 213.215 AND stack_to_pot_ratio > 0.083 AND pot_size_bb > 283.077 AND effective_stack > 13.589 AND pot_size_bb <= 293.792
**Samples:** 0
**Confidence:** 87.7%

### Rule 15: CALL
**Conditions:** stack_to_pot_ratio > 0.119 AND effective_stack <= 72.957 AND effective_stack <= 43.989 AND stack_to_pot_ratio > 0.214 AND has_been_raised <= 0.500 AND is_blind > 0.500
**Samples:** 0
**Confidence:** 87.0%

### Rule 16: CALL
**Conditions:** stack_to_pot_ratio > 0.119 AND effective_stack <= 72.957 AND effective_stack > 43.989 AND is_blind > 0.500 AND stack_size_bb > 86.915 AND position_relative_button > 0.500
**Samples:** 0
**Confidence:** 85.8%

### Rule 17: FOLD
**Conditions:** stack_to_pot_ratio <= 0.119 AND pot_size_bb <= 213.215 AND stack_to_pot_ratio <= 0.059 AND pot_size_bb <= 198.040 AND stack_to_pot_ratio <= 0.044 AND position_relative_button > 4.500
**Samples:** 1
**Confidence:** 85.7%

### Rule 18: FOLD
**Conditions:** stack_to_pot_ratio <= 0.119 AND pot_size_bb > 213.215 AND stack_to_pot_ratio > 0.083 AND pot_size_bb > 283.077 AND effective_stack <= 13.589 AND pot_size_bb > 310.550
**Samples:** 0
**Confidence:** 85.1%

### Rule 19: RAISE
**Conditions:** stack_to_pot_ratio > 0.119 AND effective_stack > 72.957 AND is_blind <= 0.500 AND pot_odds > 0.688 AND effective_stack > 86.487 AND effective_stack > 95.357
**Samples:** 0
**Confidence:** 83.5%

### Rule 20: FOLD
**Conditions:** stack_to_pot_ratio <= 0.119 AND pot_size_bb <= 213.215 AND stack_to_pot_ratio <= 0.059 AND pot_size_bb > 198.040 AND position_relative_button <= 4.500 AND position_relative_button <= 3.500
**Samples:** 1
**Confidence:** 82.9%

## Feature Importance

| Feature | Importance |
|---------|------------|
| stack_to_pot_ratio | 0.711 |
| effective_stack | 0.195 |
| is_blind | 0.047 |
| pot_odds | 0.018 |
| pot_size_bb | 0.014 |
| stack_size_bb | 0.007 |
| position_relative_button | 0.004 |
| has_been_raised | 0.002 |
| pot_commitment | 0.001 |
| players_to_act | 0.001 |
