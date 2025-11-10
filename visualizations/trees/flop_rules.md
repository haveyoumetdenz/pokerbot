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
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb <= 76.533 AND position_numeric <= 1.500 AND stack_size_bb <= 54.894
**Samples:** 1
**Confidence:** 100.0%

### Rule 2: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb <= 76.533 AND position_numeric <= 1.500 AND stack_size_bb > 54.894 AND effective_stack <= 74.544 AND hand_equity <= 0.315 AND stack_to_pot_ratio <= 0.870 AND hand_equity <= 0.285
**Samples:** 1
**Confidence:** 100.0%

### Rule 3: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb <= 76.533 AND position_numeric <= 1.500 AND stack_size_bb > 54.894 AND effective_stack <= 74.544 AND hand_equity <= 0.315 AND stack_to_pot_ratio <= 0.870 AND hand_equity > 0.285
**Samples:** 1
**Confidence:** 100.0%

### Rule 4: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb <= 76.533 AND position_numeric <= 1.500 AND stack_size_bb > 54.894 AND effective_stack > 74.544
**Samples:** 1
**Confidence:** 100.0%

### Rule 5: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb <= 76.533 AND position_numeric > 1.500 AND equity_percentile <= 36.500 AND stack_size_bb > 65.801
**Samples:** 1
**Confidence:** 100.0%

### Rule 6: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb <= 76.533 AND position_numeric > 1.500 AND equity_percentile > 36.500 AND hand_equity <= 0.355
**Samples:** 1
**Confidence:** 100.0%

### Rule 7: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb > 76.533 AND effective_stack <= 45.445
**Samples:** 1
**Confidence:** 100.0%

### Rule 8: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb > 76.533 AND effective_stack > 45.445 AND stack_size_bb <= 89.750 AND hand_equity <= 0.265
**Samples:** 1
**Confidence:** 100.0%

### Rule 9: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb > 76.533 AND effective_stack > 45.445 AND stack_size_bb <= 89.750 AND hand_equity > 0.265 AND pot_commitment <= 0.233 AND stack_to_pot_ratio <= 1.937 AND pot_size_bb <= 48.486
**Samples:** 1
**Confidence:** 100.0%

### Rule 10: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb > 76.533 AND effective_stack > 45.445 AND stack_size_bb <= 89.750 AND hand_equity > 0.265 AND pot_commitment <= 0.233 AND stack_to_pot_ratio <= 1.937 AND pot_size_bb > 48.486 AND stack_size_bb <= 88.576 AND equity_percentile <= 39.500 AND hand_equity <= 0.375 AND position_relative_button <= 0.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 11: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb > 76.533 AND effective_stack > 45.445 AND stack_size_bb <= 89.750 AND hand_equity > 0.265 AND pot_commitment <= 0.233 AND stack_to_pot_ratio <= 1.937 AND pot_size_bb > 48.486 AND stack_size_bb <= 88.576 AND equity_percentile <= 39.500 AND hand_equity > 0.375 AND effective_stack <= 78.018
**Samples:** 1
**Confidence:** 100.0%

### Rule 12: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb > 76.533 AND effective_stack > 45.445 AND stack_size_bb <= 89.750 AND hand_equity > 0.265 AND pot_commitment <= 0.233 AND stack_to_pot_ratio <= 1.937 AND pot_size_bb > 48.486 AND stack_size_bb <= 88.576 AND equity_percentile <= 39.500 AND hand_equity > 0.375 AND effective_stack > 78.018
**Samples:** 1
**Confidence:** 100.0%

### Rule 13: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb > 76.533 AND effective_stack > 45.445 AND stack_size_bb <= 89.750 AND hand_equity > 0.265 AND pot_commitment <= 0.233 AND stack_to_pot_ratio <= 1.937 AND pot_size_bb > 48.486 AND stack_size_bb > 88.576
**Samples:** 1
**Confidence:** 100.0%

### Rule 14: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb > 76.533 AND effective_stack > 45.445 AND stack_size_bb <= 89.750 AND hand_equity > 0.265 AND pot_commitment <= 0.233 AND stack_to_pot_ratio > 1.937 AND effective_stack <= 88.279 AND stack_size_bb <= 87.233 AND fold_equity > 0.150
**Samples:** 1
**Confidence:** 100.0%

### Rule 15: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb > 76.533 AND effective_stack > 45.445 AND stack_size_bb <= 89.750 AND hand_equity > 0.265 AND pot_commitment > 0.233 AND equity_percentile > 30.500 AND fold_equity <= 0.150
**Samples:** 1
**Confidence:** 100.0%

### Rule 16: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb > 76.533 AND effective_stack > 45.445 AND stack_size_bb <= 89.750 AND hand_equity > 0.265 AND pot_commitment > 0.233 AND equity_percentile > 30.500 AND fold_equity > 0.150
**Samples:** 1
**Confidence:** 100.0%

### Rule 17: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb > 76.533 AND effective_stack > 45.445 AND stack_size_bb > 89.750 AND equity_percentile <= 40.500 AND players_to_act <= 1.500 AND pot_odds <= 0.667
**Samples:** 1
**Confidence:** 100.0%

### Rule 18: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb > 76.533 AND effective_stack > 45.445 AND stack_size_bb > 89.750 AND equity_percentile <= 40.500 AND players_to_act <= 1.500 AND pot_odds > 0.667 AND equity_percentile <= 29.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 19: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb > 76.533 AND effective_stack > 45.445 AND stack_size_bb > 89.750 AND equity_percentile <= 40.500 AND players_to_act <= 1.500 AND pot_odds > 0.667 AND equity_percentile > 29.500 AND is_blind <= 0.500 AND position_relative_button <= 4.500 AND pot_size_bb <= 20.677 AND effective_stack > 98.250
**Samples:** 1
**Confidence:** 100.0%

### Rule 20: FOLD
**Conditions:** pot_size_bb <= 119.629 AND stack_size_bb > 76.533 AND effective_stack > 45.445 AND stack_size_bb > 89.750 AND equity_percentile <= 40.500 AND players_to_act <= 1.500 AND pot_odds > 0.667 AND equity_percentile > 29.500 AND is_blind <= 0.500 AND position_relative_button <= 4.500 AND pot_size_bb > 20.677
**Samples:** 1
**Confidence:** 100.0%

## Feature Importance

| Feature | Importance |
|---------|------------|
| pot_size_bb | 0.365 |
| stack_size_bb | 0.353 |
| position_numeric | 0.141 |
| equity_percentile | 0.045 |
| effective_stack | 0.040 |
| hand_equity | 0.017 |
| pot_odds | 0.011 |
| position_relative_button | 0.007 |
| players_to_act | 0.006 |
| stack_to_pot_ratio | 0.004 |
