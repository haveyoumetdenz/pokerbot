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
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile <= 18.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 2: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile <= 26.500 AND hand_equity <= 0.385 AND equity_percentile <= 22.500 AND hand_equity > 0.325 AND hand_equity <= 0.355
**Samples:** 1
**Confidence:** 100.0%

### Rule 3: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile <= 26.500 AND hand_equity <= 0.385 AND equity_percentile > 22.500 AND equity_percentile <= 23.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 4: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile <= 26.500 AND hand_equity <= 0.385 AND equity_percentile > 22.500 AND equity_percentile > 23.500 AND hand_equity <= 0.355 AND hand_equity <= 0.305 AND equity_percentile <= 25.500 AND equity_percentile <= 24.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 5: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile <= 26.500 AND hand_equity <= 0.385 AND equity_percentile > 22.500 AND equity_percentile > 23.500 AND hand_equity <= 0.355 AND hand_equity <= 0.305 AND equity_percentile > 25.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 6: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile <= 26.500 AND hand_equity <= 0.385 AND equity_percentile > 22.500 AND equity_percentile > 23.500 AND hand_equity <= 0.355 AND hand_equity > 0.305 AND hand_equity > 0.315 AND equity_percentile <= 24.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 7: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile <= 26.500 AND hand_equity <= 0.385 AND equity_percentile > 22.500 AND equity_percentile > 23.500 AND hand_equity > 0.355 AND hand_equity <= 0.375
**Samples:** 1
**Confidence:** 100.0%

### Rule 8: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile <= 26.500 AND hand_equity > 0.385 AND pot_size_bb > 200.750
**Samples:** 1
**Confidence:** 100.0%

### Rule 9: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile > 26.500 AND equity_percentile <= 40.500 AND hand_equity <= 0.395 AND hand_equity > 0.245 AND hand_equity <= 0.345 AND hand_equity <= 0.335 AND hand_equity <= 0.305 AND equity_percentile <= 34.500 AND hand_equity <= 0.255
**Samples:** 1
**Confidence:** 100.0%

### Rule 10: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile > 26.500 AND equity_percentile <= 40.500 AND hand_equity <= 0.395 AND hand_equity > 0.245 AND hand_equity <= 0.345 AND hand_equity <= 0.335 AND hand_equity > 0.305 AND equity_percentile <= 37.500 AND hand_equity <= 0.315 AND equity_percentile <= 28.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 11: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile > 26.500 AND equity_percentile <= 40.500 AND hand_equity <= 0.395 AND hand_equity > 0.245 AND hand_equity <= 0.345 AND hand_equity <= 0.335 AND hand_equity > 0.305 AND equity_percentile > 37.500 AND equity_percentile > 38.500 AND hand_equity <= 0.315
**Samples:** 1
**Confidence:** 100.0%

### Rule 12: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile > 26.500 AND equity_percentile <= 40.500 AND hand_equity <= 0.395 AND hand_equity > 0.245 AND hand_equity <= 0.345 AND hand_equity > 0.335 AND pot_size_bb <= 200.750 AND equity_percentile <= 35.500 AND equity_percentile > 33.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 13: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile > 26.500 AND equity_percentile <= 40.500 AND hand_equity <= 0.395 AND hand_equity > 0.245 AND hand_equity <= 0.345 AND hand_equity > 0.335 AND pot_size_bb > 200.750 AND equity_percentile <= 30.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 14: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile > 26.500 AND equity_percentile <= 40.500 AND hand_equity <= 0.395 AND hand_equity > 0.245 AND hand_equity <= 0.345 AND hand_equity > 0.335 AND pot_size_bb > 200.750 AND equity_percentile > 30.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 15: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile > 26.500 AND equity_percentile <= 40.500 AND hand_equity <= 0.395 AND hand_equity > 0.245 AND hand_equity > 0.345 AND equity_percentile <= 39.500 AND equity_percentile <= 37.500 AND equity_percentile <= 36.500 AND hand_equity > 0.385 AND equity_percentile > 32.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 16: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile > 26.500 AND equity_percentile <= 40.500 AND hand_equity <= 0.395 AND hand_equity > 0.245 AND hand_equity > 0.345 AND equity_percentile <= 39.500 AND equity_percentile <= 37.500 AND equity_percentile > 36.500 AND hand_equity <= 0.355
**Samples:** 1
**Confidence:** 100.0%

### Rule 17: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile > 26.500 AND equity_percentile <= 40.500 AND hand_equity > 0.395 AND hand_equity <= 0.415 AND equity_percentile > 32.500 AND hand_equity <= 0.405
**Samples:** 1
**Confidence:** 100.0%

### Rule 18: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile > 26.500 AND equity_percentile <= 40.500 AND hand_equity > 0.395 AND hand_equity <= 0.415 AND equity_percentile > 32.500 AND hand_equity > 0.405
**Samples:** 1
**Confidence:** 100.0%

### Rule 19: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile > 26.500 AND equity_percentile <= 40.500 AND hand_equity > 0.395 AND hand_equity > 0.415 AND hand_equity > 0.425 AND hand_equity <= 0.435
**Samples:** 1
**Confidence:** 100.0%

### Rule 20: FOLD
**Conditions:** effective_stack <= 0.500 AND pot_size_bb <= 323.042 AND stack_size_bb <= 0.497 AND pot_size_bb <= 240.001 AND fold_equity <= 0.150 AND position_relative_button <= 2.500 AND pot_size_bb <= 221.791 AND pot_size_bb <= 201.875 AND pot_size_bb > 200.250 AND pot_size_bb <= 201.005 AND equity_percentile <= 48.500 AND equity_percentile > 18.500 AND equity_percentile > 26.500 AND equity_percentile > 40.500 AND hand_equity <= 0.285
**Samples:** 1
**Confidence:** 100.0%

## Feature Importance

| Feature | Importance |
|---------|------------|
| effective_stack | 0.520 |
| pot_size_bb | 0.249 |
| stack_size_bb | 0.084 |
| equity_percentile | 0.048 |
| hand_equity | 0.043 |
| stack_to_pot_ratio | 0.020 |
| position_relative_button | 0.010 |
| fold_equity | 0.008 |
| pot_odds | 0.006 |
| is_blind | 0.003 |
