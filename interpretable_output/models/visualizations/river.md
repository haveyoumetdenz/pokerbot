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
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric <= 1.500 AND pot_size_bb <= 201.568 AND stack_to_pot_ratio <= 0.030 AND is_button <= 0.500 AND position_numeric <= 0.500 AND pot_size_bb <= 200.998 AND stack_size_bb <= 1.012 AND effective_stack <= 0.299
**Samples:** 1
**Confidence:** 100.0%

### Rule 2: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric <= 1.500 AND pot_size_bb <= 201.568 AND stack_to_pot_ratio <= 0.030 AND is_button <= 0.500 AND position_numeric > 0.500 AND position_relative_button > 2.500 AND pot_size_bb <= 201.451 AND stack_size_bb <= 0.310
**Samples:** 1
**Confidence:** 100.0%

### Rule 3: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric <= 1.500 AND pot_size_bb <= 201.568 AND stack_to_pot_ratio <= 0.030 AND is_button > 0.500 AND pot_size_bb > 200.706 AND pot_size_bb <= 201.056 AND equity_percentile <= 24.500 AND equity_percentile > 22.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 4: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric <= 1.500 AND pot_size_bb <= 201.568 AND stack_to_pot_ratio > 0.030 AND pot_size_bb <= 189.247 AND pot_size_bb <= 183.277
**Samples:** 1
**Confidence:** 100.0%

### Rule 5: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric <= 1.500 AND pot_size_bb <= 201.568 AND stack_to_pot_ratio > 0.030 AND pot_size_bb > 189.247 AND effective_stack <= 5.477 AND stack_size_bb <= 7.607 AND hand_equity <= 0.275 AND stack_size_bb <= 6.680
**Samples:** 1
**Confidence:** 100.0%

### Rule 6: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric <= 1.500 AND pot_size_bb <= 201.568 AND stack_to_pot_ratio > 0.030 AND pot_size_bb > 189.247 AND effective_stack <= 5.477 AND stack_size_bb > 7.607 AND pot_size_bb <= 191.892
**Samples:** 1
**Confidence:** 100.0%

### Rule 7: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric <= 1.500 AND pot_size_bb <= 201.568 AND stack_to_pot_ratio > 0.030 AND pot_size_bb > 189.247 AND effective_stack > 5.477 AND pot_size_bb <= 199.378 AND equity_percentile <= 20.500 AND equity_percentile <= 18.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 8: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric <= 1.500 AND pot_size_bb > 201.568 AND is_blind <= 0.500 AND position_relative_button <= 2.500 AND pot_size_bb > 206.126 AND pot_size_bb > 209.251 AND effective_stack > 0.136 AND hand_equity > 0.365
**Samples:** 1
**Confidence:** 100.0%

### Rule 9: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric <= 1.500 AND pot_size_bb > 201.568 AND is_blind <= 0.500 AND position_relative_button > 2.500 AND pot_size_bb <= 206.735 AND effective_stack <= 6.501 AND pot_size_bb <= 203.157 AND pot_size_bb <= 201.647
**Samples:** 1
**Confidence:** 100.0%

### Rule 10: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric <= 1.500 AND pot_size_bb > 201.568 AND is_blind > 0.500 AND position_relative_button <= 0.500 AND pot_size_bb <= 202.850 AND pot_size_bb > 202.011 AND equity_percentile <= 40.500 AND pot_odds <= 0.002
**Samples:** 1
**Confidence:** 100.0%

### Rule 11: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric > 1.500 AND pot_size_bb <= 205.002 AND pot_size_bb <= 195.244 AND stack_to_pot_ratio > 0.019 AND stack_to_pot_ratio > 0.049 AND effective_stack > 9.069 AND pot_size_bb <= 187.662
**Samples:** 1
**Confidence:** 100.0%

### Rule 12: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric > 1.500 AND pot_size_bb <= 205.002 AND pot_size_bb > 195.244 AND pot_size_bb <= 201.498 AND stack_size_bb <= 0.179
**Samples:** 1
**Confidence:** 100.0%

### Rule 13: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric > 1.500 AND pot_size_bb <= 205.002 AND pot_size_bb > 195.244 AND pot_size_bb <= 201.498 AND stack_size_bb > 0.179 AND effective_stack <= 3.788 AND effective_stack <= 1.500 AND hand_equity > 0.425
**Samples:** 1
**Confidence:** 100.0%

### Rule 14: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric > 1.500 AND pot_size_bb <= 205.002 AND pot_size_bb > 195.244 AND pot_size_bb > 201.498 AND pot_size_bb > 201.515 AND pot_size_bb <= 202.020 AND equity_percentile > 19.500 AND equity_percentile <= 21.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 15: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric > 1.500 AND pot_size_bb > 205.002 AND pot_size_bb <= 210.630 AND stack_size_bb <= 0.176 AND pot_size_bb > 208.325 AND pot_size_bb <= 208.439 AND pot_size_bb > 208.420 AND equity_percentile <= 31.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 16: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric > 1.500 AND pot_size_bb > 205.002 AND pot_size_bb <= 210.630 AND stack_size_bb <= 0.176 AND pot_size_bb > 208.325 AND pot_size_bb <= 208.439 AND pot_size_bb > 208.420 AND equity_percentile > 31.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 17: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric > 1.500 AND pot_size_bb > 205.002 AND pot_size_bb <= 210.630 AND stack_size_bb > 0.176 AND stack_size_bb <= 1.378 AND pot_size_bb > 205.334 AND hand_equity <= 0.335 AND hand_equity > 0.295
**Samples:** 1
**Confidence:** 100.0%

### Rule 18: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric > 1.500 AND pot_size_bb > 205.002 AND pot_size_bb > 210.630 AND pot_size_bb <= 210.923 AND pot_size_bb <= 210.750 AND pot_size_bb <= 210.716 AND equity_percentile > 31.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 19: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric > 1.500 AND pot_size_bb > 205.002 AND pot_size_bb > 210.630 AND pot_size_bb <= 210.923 AND pot_size_bb > 210.750 AND pot_size_bb <= 210.906 AND hand_equity <= 0.345 AND equity_percentile <= 28.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 20: FOLD
**Conditions:** stack_to_pot_ratio <= 0.111 AND pot_size_bb <= 213.649 AND stack_to_pot_ratio <= 0.049 AND position_relative_button <= 4.500 AND position_numeric > 1.500 AND pot_size_bb > 205.002 AND pot_size_bb > 210.630 AND pot_size_bb <= 210.923 AND pot_size_bb > 210.750 AND pot_size_bb <= 210.906 AND hand_equity <= 0.345 AND equity_percentile > 28.500
**Samples:** 1
**Confidence:** 100.0%

## Feature Importance

| Feature | Importance |
|---------|------------|
| stack_to_pot_ratio | 0.666 |
| effective_stack | 0.171 |
| pot_size_bb | 0.045 |
| pot_odds | 0.036 |
| position_relative_button | 0.020 |
| stack_size_bb | 0.020 |
| equity_percentile | 0.011 |
| is_blind | 0.011 |
| hand_equity | 0.008 |
| players_remaining | 0.005 |
