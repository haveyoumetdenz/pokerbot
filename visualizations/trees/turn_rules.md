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
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio <= 0.973 AND equity_percentile <= 27.500 AND position_relative_button <= 4.500 AND stack_size_bb <= 33.446
**Samples:** 1
**Confidence:** 100.0%

### Rule 2: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio <= 0.973 AND equity_percentile <= 27.500 AND position_relative_button <= 4.500 AND stack_size_bb > 33.446 AND fold_equity <= 0.150 AND pot_size_bb > 111.529 AND pot_size_bb > 126.720 AND effective_stack <= 21.869
**Samples:** 1
**Confidence:** 100.0%

### Rule 3: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio <= 0.973 AND equity_percentile <= 27.500 AND position_relative_button <= 4.500 AND stack_size_bb > 33.446 AND fold_equity <= 0.150 AND pot_size_bb > 111.529 AND pot_size_bb > 126.720 AND effective_stack > 21.869
**Samples:** 1
**Confidence:** 100.0%

### Rule 4: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio <= 0.973 AND equity_percentile <= 27.500 AND position_relative_button > 4.500 AND pot_size_bb > 121.976
**Samples:** 1
**Confidence:** 100.0%

### Rule 5: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio <= 0.973 AND equity_percentile > 27.500 AND stack_to_pot_ratio <= 0.730 AND stack_to_pot_ratio <= 0.549 AND pot_size_bb <= 142.773 AND equity_percentile <= 34.500 AND pot_commitment <= 0.233
**Samples:** 1
**Confidence:** 100.0%

### Rule 6: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio <= 0.973 AND equity_percentile > 27.500 AND stack_to_pot_ratio <= 0.730 AND stack_to_pot_ratio <= 0.549 AND pot_size_bb <= 142.773 AND equity_percentile > 34.500 AND fold_equity <= 0.150
**Samples:** 1
**Confidence:** 100.0%

### Rule 7: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio <= 0.973 AND equity_percentile > 27.500 AND stack_to_pot_ratio <= 0.730 AND stack_to_pot_ratio <= 0.549 AND pot_size_bb <= 142.773 AND equity_percentile > 34.500 AND fold_equity > 0.150 AND effective_stack <= 41.065
**Samples:** 1
**Confidence:** 100.0%

### Rule 8: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio <= 0.973 AND equity_percentile > 27.500 AND stack_to_pot_ratio <= 0.730 AND stack_to_pot_ratio <= 0.549 AND pot_size_bb > 142.773 AND position_numeric <= 0.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 9: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio <= 0.973 AND equity_percentile > 27.500 AND stack_to_pot_ratio <= 0.730 AND stack_to_pot_ratio <= 0.549 AND pot_size_bb > 142.773 AND position_numeric > 0.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 10: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio <= 0.973 AND equity_percentile > 27.500 AND stack_to_pot_ratio <= 0.730 AND stack_to_pot_ratio > 0.549 AND pot_commitment <= 0.144 AND effective_stack <= 60.567 AND stack_size_bb <= 78.889 AND equity_percentile <= 39.500 AND position_numeric <= 0.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 11: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio <= 0.973 AND equity_percentile > 27.500 AND stack_to_pot_ratio <= 0.730 AND stack_to_pot_ratio > 0.549 AND pot_commitment <= 0.144 AND effective_stack <= 60.567 AND stack_size_bb > 78.889 AND pot_size_bb > 124.762
**Samples:** 1
**Confidence:** 100.0%

### Rule 12: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio <= 0.973 AND equity_percentile > 27.500 AND stack_to_pot_ratio <= 0.730 AND stack_to_pot_ratio > 0.549 AND pot_commitment <= 0.144 AND effective_stack > 60.567 AND players_remaining <= 2.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 13: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio <= 0.973 AND equity_percentile > 27.500 AND stack_to_pot_ratio > 0.730 AND effective_stack <= 39.607
**Samples:** 1
**Confidence:** 100.0%

### Rule 14: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio <= 0.973 AND equity_percentile > 27.500 AND stack_to_pot_ratio > 0.730 AND effective_stack > 39.607 AND stack_size_bb <= 74.292 AND effective_stack > 63.359 AND pot_size_bb > 77.368 AND equity_percentile <= 32.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 15: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio <= 0.973 AND equity_percentile > 27.500 AND stack_to_pot_ratio > 0.730 AND effective_stack > 39.607 AND stack_size_bb > 74.292 AND hand_equity > 0.345
**Samples:** 1
**Confidence:** 100.0%

### Rule 16: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio > 0.973 AND stack_size_bb <= 87.718 AND effective_stack <= 83.712 AND stack_size_bb > 71.799 AND pot_commitment <= 0.288 AND stack_size_bb <= 85.218 AND pot_odds <= 0.013 AND stack_size_bb > 79.659
**Samples:** 1
**Confidence:** 100.0%

### Rule 17: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio > 0.973 AND stack_size_bb <= 87.718 AND effective_stack <= 83.712 AND stack_size_bb > 71.799 AND pot_commitment > 0.288
**Samples:** 1
**Confidence:** 100.0%

### Rule 18: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio > 0.973 AND stack_size_bb <= 87.718 AND effective_stack > 83.712 AND hand_equity <= 0.345 AND position_relative_button > 2.500 AND pot_size_bb > 40.936
**Samples:** 1
**Confidence:** 100.0%

### Rule 19: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio > 0.973 AND stack_size_bb > 87.718 AND position_relative_button <= 1.500 AND pot_size_bb <= 24.442 AND stack_to_pot_ratio <= 7.728 AND equity_percentile > 26.500 AND stack_to_pot_ratio > 5.701
**Samples:** 1
**Confidence:** 100.0%

### Rule 20: FOLD
**Conditions:** pot_size_bb <= 178.771 AND stack_to_pot_ratio > 0.973 AND stack_size_bb > 87.718 AND position_relative_button <= 1.500 AND pot_size_bb <= 24.442 AND stack_to_pot_ratio > 7.728 AND effective_stack <= 96.875
**Samples:** 1
**Confidence:** 100.0%

## Feature Importance

| Feature | Importance |
|---------|------------|
| pot_size_bb | 0.433 |
| stack_to_pot_ratio | 0.303 |
| stack_size_bb | 0.086 |
| effective_stack | 0.054 |
| hand_equity | 0.051 |
| equity_percentile | 0.040 |
| pot_commitment | 0.013 |
| position_relative_button | 0.008 |
| fold_equity | 0.006 |
| pot_odds | 0.003 |
