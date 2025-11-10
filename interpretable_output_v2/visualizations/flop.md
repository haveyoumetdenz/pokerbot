# Flop Decision Tree Rules

## Overview
This document contains the decision rules learned by the interpretable poker AI for flop betting rounds.

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
**Conditions:** effective_stack <= 38.000 AND effective_stack > 6.254 AND stack_size_bb > 39.007 AND pot_odds > 0.163 AND pot_commitment > 0.283 AND effective_stack > 28.883 AND pot_odds > 0.241 AND current_bet_bb > 27.477
**Samples:** 1
**Confidence:** 100.0%

### Rule 2: RAISE
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack <= 44.252 AND stack_size_bb > 84.644 AND pot_size_bb <= 86.584 AND stack_size_bb <= 87.875 AND stack_to_pot_ratio > 1.002 AND position_numeric <= 0.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 3: RAISE
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack <= 44.252 AND stack_size_bb > 84.644 AND pot_size_bb <= 86.584 AND stack_size_bb <= 87.875 AND stack_to_pot_ratio > 1.002 AND position_numeric > 0.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 4: FOLD
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack <= 44.252 AND stack_size_bb > 84.644 AND pot_size_bb <= 86.584 AND stack_size_bb > 87.875 AND pot_size_bb <= 85.125
**Samples:** 1
**Confidence:** 100.0%

### Rule 5: FOLD
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack <= 44.252 AND stack_size_bb > 84.644 AND pot_size_bb <= 86.584 AND stack_size_bb > 87.875 AND pot_size_bb > 85.125
**Samples:** 1
**Confidence:** 100.0%

### Rule 6: RAISE
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack <= 44.252 AND stack_size_bb > 84.644 AND pot_size_bb > 86.584 AND effective_stack > 43.264 AND stack_size_bb <= 88.026 AND stack_size_bb <= 87.007
**Samples:** 1
**Confidence:** 100.0%

### Rule 7: FOLD
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack > 44.252 AND stack_size_bb > 59.813 AND stack_to_pot_ratio <= 0.666 AND stack_size_bb > 90.701 AND effective_stack <= 45.938 AND equity_percentile > 30.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 8: FOLD
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack > 44.252 AND stack_size_bb > 59.813 AND stack_to_pot_ratio > 0.666 AND effective_stack <= 46.515 AND stack_size_bb > 91.509 AND effective_stack <= 45.813
**Samples:** 1
**Confidence:** 100.0%

### Rule 9: FOLD
**Conditions:** effective_stack <= 38.000 AND effective_stack <= 6.254 AND pot_odds <= 0.155 AND stack_to_pot_ratio <= 0.021 AND pot_size_bb > 390.962 AND effective_stack <= 0.500 AND pot_size_bb > 485.300 AND stack_to_pot_ratio <= 0.014
**Samples:** 1
**Confidence:** 100.0%

### Rule 10: RAISE
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack > 44.252 AND stack_size_bb > 59.813 AND stack_to_pot_ratio > 0.666 AND effective_stack > 46.515 AND stack_to_pot_ratio > 1.222 AND players_to_act <= 2.500
**Samples:** 0
**Confidence:** 99.8%

### Rule 11: FOLD
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack <= 44.252 AND stack_size_bb > 84.644 AND pot_size_bb > 86.584 AND effective_stack > 43.264 AND stack_size_bb > 88.026 AND position_relative_button <= 4.500
**Samples:** 0
**Confidence:** 99.3%

### Rule 12: RAISE
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack > 44.252 AND stack_size_bb > 59.813 AND stack_to_pot_ratio > 0.666 AND effective_stack > 46.515 AND stack_to_pot_ratio > 1.222 AND players_to_act > 2.500
**Samples:** 0
**Confidence:** 99.3%

### Rule 13: RAISE
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack <= 44.252 AND stack_size_bb <= 84.644 AND stack_size_bb > 55.272 AND stack_size_bb <= 79.450 AND pot_size_bb <= 116.006 AND stack_size_bb > 59.891
**Samples:** 1
**Confidence:** 99.2%

### Rule 14: FOLD
**Conditions:** effective_stack <= 38.000 AND effective_stack <= 6.254 AND pot_odds > 0.155 AND stack_size_bb > 58.068 AND pot_odds > 0.262 AND stack_to_pot_ratio > 0.537 AND players_remaining <= 2.500 AND stack_size_bb > 84.563
**Samples:** 0
**Confidence:** 99.1%

### Rule 15: RAISE
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack <= 44.252 AND stack_size_bb <= 84.644 AND stack_size_bb > 55.272 AND stack_size_bb > 79.450 AND effective_stack > 40.943 AND effective_stack > 41.594
**Samples:** 1
**Confidence:** 99.1%

### Rule 16: RAISE
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack > 44.252 AND stack_size_bb > 59.813 AND stack_to_pot_ratio > 0.666 AND effective_stack > 46.515 AND stack_to_pot_ratio <= 1.222 AND stack_size_bb <= 96.562
**Samples:** 0
**Confidence:** 98.9%

### Rule 17: RAISE
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack > 44.252 AND stack_size_bb > 59.813 AND stack_to_pot_ratio > 0.666 AND effective_stack <= 46.515 AND stack_size_bb <= 91.509 AND stack_size_bb <= 90.047
**Samples:** 0
**Confidence:** 98.9%

### Rule 18: FOLD
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack <= 44.252 AND stack_size_bb > 84.644 AND pot_size_bb > 86.584 AND effective_stack <= 43.264 AND current_bet_bb <= 12.735 AND pot_size_bb <= 204.958
**Samples:** 0
**Confidence:** 98.2%

### Rule 19: RAISE
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack <= 44.252 AND stack_size_bb <= 84.644 AND stack_size_bb > 55.272 AND stack_size_bb <= 79.450 AND pot_size_bb <= 116.006 AND stack_size_bb <= 59.891
**Samples:** 1
**Confidence:** 97.9%

### Rule 20: FOLD
**Conditions:** effective_stack > 38.000 AND stack_to_pot_ratio > 0.324 AND effective_stack <= 44.252 AND stack_size_bb <= 84.644 AND stack_size_bb > 55.272 AND stack_size_bb > 79.450 AND effective_stack <= 40.943 AND effective_stack <= 39.996
**Samples:** 0
**Confidence:** 97.9%

## Feature Importance

| Feature | Importance |
|---------|------------|
| effective_stack | 0.803 |
| stack_size_bb | 0.076 |
| pot_odds | 0.060 |
| stack_to_pot_ratio | 0.046 |
| pot_size_bb | 0.009 |
| players_to_act | 0.002 |
| current_bet_bb | 0.002 |
| fold_equity | 0.001 |
| pot_commitment | 0.001 |
| players_remaining | 0.001 |
