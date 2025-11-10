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
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb <= 196.570 AND effective_stack <= 1.430 AND stack_to_pot_ratio <= 0.052 AND pot_size_bb <= 195.524 AND pot_size_bb <= 194.982 AND pot_size_bb > 192.325 AND equity_percentile > 32.500 AND is_blind > 0.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 2: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb <= 196.570 AND effective_stack > 1.430 AND pot_size_bb <= 190.501 AND stack_size_bb <= 9.571 AND pot_size_bb <= 183.081
**Samples:** 1
**Confidence:** 100.0%

### Rule 3: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb <= 196.570 AND effective_stack > 1.430 AND pot_size_bb > 190.501 AND is_button <= 0.500 AND hand_equity <= 0.395 AND position_relative_button > 2.500 AND stack_size_bb > 10.221 AND stack_size_bb > 10.284
**Samples:** 1
**Confidence:** 100.0%

### Rule 4: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb <= 196.570 AND effective_stack > 1.430 AND pot_size_bb > 190.501 AND is_button > 0.500 AND stack_to_pot_ratio > 0.042 AND stack_to_pot_ratio <= 0.048 AND effective_stack > 8.618
**Samples:** 1
**Confidence:** 100.0%

### Rule 5: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb > 196.570 AND position_relative_button <= 0.500 AND pot_size_bb <= 200.504 AND stack_size_bb > 1.529 AND stack_to_pot_ratio <= 0.018
**Samples:** 1
**Confidence:** 100.0%

### Rule 6: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb > 196.570 AND position_relative_button <= 0.500 AND pot_size_bb > 200.504 AND pot_size_bb <= 201.494 AND equity_percentile <= 35.500 AND hand_equity <= 0.335 AND hand_equity <= 0.305 AND equity_percentile <= 32.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 7: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb > 196.570 AND position_relative_button <= 0.500 AND pot_size_bb > 200.504 AND pot_size_bb <= 201.494 AND equity_percentile <= 35.500 AND hand_equity <= 0.335 AND hand_equity > 0.305 AND equity_percentile > 30.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 8: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb > 196.570 AND position_relative_button <= 0.500 AND pot_size_bb > 200.504 AND pot_size_bb <= 201.494 AND equity_percentile <= 35.500 AND hand_equity > 0.335
**Samples:** 1
**Confidence:** 100.0%

### Rule 9: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb > 196.570 AND position_relative_button <= 0.500 AND pot_size_bb > 200.504 AND pot_size_bb <= 201.494 AND equity_percentile > 35.500 AND hand_equity <= 0.305
**Samples:** 1
**Confidence:** 100.0%

### Rule 10: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb > 196.570 AND position_relative_button <= 0.500 AND pot_size_bb > 200.504 AND pot_size_bb > 201.494 AND pot_size_bb > 206.749 AND pot_size_bb > 212.002 AND pot_size_bb <= 212.497
**Samples:** 1
**Confidence:** 100.0%

### Rule 11: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb > 196.570 AND position_relative_button <= 0.500 AND pot_size_bb > 200.504 AND pot_size_bb > 201.494 AND pot_size_bb > 206.749 AND pot_size_bb > 212.002 AND pot_size_bb > 212.497 AND hand_equity <= 0.315
**Samples:** 1
**Confidence:** 100.0%

### Rule 12: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb > 196.570 AND position_relative_button > 0.500 AND position_numeric <= 0.500 AND pot_size_bb <= 200.390 AND pot_size_bb <= 199.959 AND hand_equity > 0.275 AND pot_size_bb <= 196.967
**Samples:** 1
**Confidence:** 100.0%

### Rule 13: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb > 196.570 AND position_relative_button > 0.500 AND position_numeric <= 0.500 AND pot_size_bb <= 200.390 AND pot_size_bb > 199.959
**Samples:** 1
**Confidence:** 100.0%

### Rule 14: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb > 196.570 AND position_relative_button > 0.500 AND position_numeric <= 0.500 AND pot_size_bb > 200.390 AND pot_size_bb > 201.817 AND pot_size_bb <= 202.489 AND equity_percentile <= 21.500 AND hand_equity <= 0.335
**Samples:** 1
**Confidence:** 100.0%

### Rule 15: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb > 196.570 AND position_relative_button > 0.500 AND position_numeric > 0.500 AND position_relative_button <= 4.500 AND position > 1.500 AND pot_size_bb <= 201.033 AND stack_to_pot_ratio <= 0.020
**Samples:** 1
**Confidence:** 100.0%

### Rule 16: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb > 196.570 AND position_relative_button > 0.500 AND position_numeric > 0.500 AND position_relative_button > 4.500 AND pot_size_bb <= 201.108 AND pot_size_bb <= 200.700 AND stack_to_pot_ratio <= 0.012
**Samples:** 1
**Confidence:** 100.0%

### Rule 17: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio <= 0.054 AND pot_size_bb > 196.570 AND position_relative_button > 0.500 AND position_numeric > 0.500 AND position_relative_button > 4.500 AND pot_size_bb > 201.108 AND pot_size_bb <= 201.656 AND pot_size_bb > 201.478
**Samples:** 1
**Confidence:** 100.0%

### Rule 18: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio > 0.054 AND pot_size_bb <= 184.648 AND position_relative_button <= 4.500 AND pot_size_bb > 179.501 AND effective_stack > 9.445 AND pot_size_bb <= 180.779 AND effective_stack > 16.680 AND equity_percentile <= 31.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 19: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio > 0.054 AND pot_size_bb <= 184.648 AND position_relative_button > 4.500 AND stack_to_pot_ratio <= 0.075 AND pot_size_bb <= 182.648 AND hand_equity <= 0.355 AND total_street_bets <= 0.500 AND pot_size_bb <= 181.183
**Samples:** 1
**Confidence:** 100.0%

### Rule 20: FOLD
**Conditions:** stack_to_pot_ratio <= 0.139 AND stack_to_pot_ratio <= 0.099 AND pot_size_bb <= 213.194 AND stack_to_pot_ratio > 0.054 AND pot_size_bb <= 184.648 AND position_relative_button > 4.500 AND stack_to_pot_ratio <= 0.075 AND pot_size_bb <= 182.648 AND hand_equity > 0.355 AND equity_percentile <= 33.500 AND pot_size_bb <= 178.510
**Samples:** 1
**Confidence:** 100.0%

## Feature Importance

| Feature | Importance |
|---------|------------|
| stack_to_pot_ratio | 0.708 |
| effective_stack | 0.143 |
| position_relative_button | 0.059 |
| total_street_bets | 0.027 |
| pot_size_bb | 0.020 |
| stack_size_bb | 0.010 |
| players_remaining | 0.006 |
| equity_percentile | 0.005 |
| pot_odds | 0.005 |
| hand_equity | 0.004 |
