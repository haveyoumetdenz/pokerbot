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
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb <= 64.414 AND equity_percentile <= 25.500 AND pot_size_bb > 119.627 AND effective_stack <= 34.898
**Samples:** 1
**Confidence:** 100.0%

### Rule 2: FOLD
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb <= 64.414 AND equity_percentile <= 25.500 AND pot_size_bb > 119.627 AND effective_stack > 34.898
**Samples:** 1
**Confidence:** 100.0%

### Rule 3: FOLD
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb <= 64.414 AND equity_percentile > 25.500 AND stack_size_bb <= 47.105 AND stack_to_pot_ratio <= 0.231
**Samples:** 1
**Confidence:** 100.0%

### Rule 4: FOLD
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb <= 64.414 AND equity_percentile > 25.500 AND stack_size_bb <= 47.105 AND stack_to_pot_ratio > 0.231 AND hand_equity <= 0.295
**Samples:** 1
**Confidence:** 100.0%

### Rule 5: FOLD
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb <= 64.414 AND equity_percentile > 25.500 AND stack_size_bb <= 47.105 AND stack_to_pot_ratio > 0.231 AND hand_equity > 0.295 AND stack_size_bb <= 39.300 AND effective_stack > 34.170
**Samples:** 1
**Confidence:** 100.0%

### Rule 6: FOLD
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb <= 64.414 AND equity_percentile > 25.500 AND stack_size_bb > 47.105 AND stack_size_bb <= 60.350 AND hand_equity <= 0.385 AND effective_stack <= 56.611 AND pot_size_bb > 97.827 AND stack_to_pot_ratio <= 0.470 AND pot_size_bb > 115.125 AND pot_odds > 0.291
**Samples:** 1
**Confidence:** 100.0%

### Rule 7: FOLD
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb > 64.414 AND position_relative_button <= 4.500 AND pot_size_bb <= 82.883 AND fold_equity <= 0.150 AND effective_stack > 68.987 AND equity_percentile <= 33.500 AND stack_size_bb > 96.594
**Samples:** 1
**Confidence:** 100.0%

### Rule 8: FOLD
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb > 64.414 AND position_relative_button <= 4.500 AND pot_size_bb <= 82.883 AND fold_equity <= 0.150 AND effective_stack > 68.987 AND equity_percentile > 33.500 AND equity_percentile > 35.500 AND hand_equity > 0.325 AND effective_stack > 91.034 AND stack_to_pot_ratio <= 6.764
**Samples:** 1
**Confidence:** 100.0%

### Rule 9: FOLD
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb > 64.414 AND position_relative_button <= 4.500 AND pot_size_bb <= 82.883 AND fold_equity > 0.150 AND stack_to_pot_ratio > 1.024 AND stack_to_pot_ratio > 1.076 AND effective_stack <= 77.034 AND stack_size_bb <= 83.954 AND hand_equity <= 0.355 AND equity_percentile > 33.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 10: FOLD
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb > 64.414 AND position_relative_button <= 4.500 AND pot_size_bb <= 82.883 AND fold_equity > 0.150 AND stack_to_pot_ratio > 1.024 AND stack_to_pot_ratio > 1.076 AND effective_stack <= 77.034 AND stack_size_bb > 83.954
**Samples:** 1
**Confidence:** 100.0%

### Rule 11: FOLD
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb > 64.414 AND position_relative_button <= 4.500 AND pot_size_bb <= 82.883 AND fold_equity > 0.150 AND stack_to_pot_ratio > 1.024 AND stack_to_pot_ratio > 1.076 AND effective_stack > 77.034 AND stack_to_pot_ratio > 4.331 AND position_relative_button > 0.500 AND hand_equity > 0.335 AND equity_percentile <= 37.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 12: FOLD
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb > 64.414 AND position_relative_button <= 4.500 AND pot_size_bb > 82.883 AND pot_size_bb <= 101.209 AND stack_size_bb > 72.635
**Samples:** 1
**Confidence:** 100.0%

### Rule 13: FOLD
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb > 64.414 AND position_relative_button <= 4.500 AND pot_size_bb > 82.883 AND pot_size_bb > 101.209 AND stack_size_bb > 65.845
**Samples:** 1
**Confidence:** 100.0%

### Rule 14: FOLD
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb > 64.414 AND position_relative_button > 4.500 AND effective_stack <= 40.066
**Samples:** 1
**Confidence:** 100.0%

### Rule 15: FOLD
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb > 64.414 AND position_relative_button > 4.500 AND effective_stack > 40.066 AND hand_equity <= 0.295
**Samples:** 1
**Confidence:** 100.0%

### Rule 16: FOLD
**Conditions:** pot_size_bb > 148.100 AND pot_size_bb <= 164.101 AND pot_size_bb <= 163.250 AND pot_odds <= 0.003
**Samples:** 1
**Confidence:** 100.0%

### Rule 17: FOLD
**Conditions:** pot_size_bb > 148.100 AND pot_size_bb <= 164.101 AND pot_size_bb <= 163.250 AND pot_odds > 0.003
**Samples:** 1
**Confidence:** 100.0%

### Rule 18: FOLD
**Conditions:** pot_size_bb > 148.100 AND pot_size_bb > 164.101
**Samples:** 1
**Confidence:** 100.0%

### Rule 19: CALL
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb <= 64.414 AND equity_percentile > 25.500 AND stack_size_bb <= 47.105 AND stack_to_pot_ratio > 0.231 AND hand_equity > 0.295 AND stack_size_bb > 39.300 AND equity_percentile > 37.500
**Samples:** 0
**Confidence:** 98.2%

### Rule 20: CALL
**Conditions:** pot_size_bb <= 148.100 AND stack_size_bb <= 64.414 AND equity_percentile > 25.500 AND stack_size_bb > 47.105 AND stack_size_bb > 60.350 AND pot_size_bb <= 81.789
**Samples:** 0
**Confidence:** 97.9%

## Feature Importance

| Feature | Importance |
|---------|------------|
| pot_size_bb | 0.530 |
| stack_size_bb | 0.159 |
| effective_stack | 0.068 |
| stack_to_pot_ratio | 0.067 |
| position_relative_button | 0.060 |
| equity_percentile | 0.057 |
| hand_equity | 0.038 |
| fold_equity | 0.019 |
| pot_odds | 0.002 |
| position | 0.000 |
