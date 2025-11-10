# Preflop Decision Tree Rules

## Overview
This document contains the decision rules learned by the interpretable poker AI for preflop betting rounds.

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
**Conditions:** effective_stack <= 33.306
**Samples:** 1
**Confidence:** 100.0%

### Rule 2: FOLD
**Conditions:** effective_stack > 33.306 AND pot_odds <= 0.288 AND players_to_act <= 4.500 AND position_relative_button <= 4.500 AND pot_size_bb <= 170.972 AND position_relative_button > 2.500 AND position_relative_button <= 3.500 AND hand_equity > 0.315 AND pot_commitment > 0.064 AND effective_stack <= 93.386 AND current_bet_bb <= 13.112
**Samples:** 1
**Confidence:** 100.0%

### Rule 3: FOLD
**Conditions:** effective_stack > 33.306 AND pot_odds <= 0.288 AND players_to_act <= 4.500 AND position_relative_button <= 4.500 AND pot_size_bb <= 170.972 AND position_relative_button > 2.500 AND position_relative_button > 3.500 AND equity_percentile > 29.500 AND pot_odds > 0.269
**Samples:** 1
**Confidence:** 100.0%

### Rule 4: FOLD
**Conditions:** effective_stack > 33.306 AND pot_odds <= 0.288 AND players_to_act <= 4.500 AND position_relative_button > 4.500 AND hand_equity <= 0.405 AND pot_commitment <= 0.156 AND effective_stack <= 47.039
**Samples:** 1
**Confidence:** 100.0%

### Rule 5: FOLD
**Conditions:** effective_stack > 33.306 AND pot_odds > 0.288 AND pot_odds <= 0.700 AND hand_equity <= 0.335 AND position_relative_button <= 2.500 AND is_blind > 0.500 AND equity_percentile > 34.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 6: FOLD
**Conditions:** effective_stack > 33.306 AND pot_odds > 0.288 AND pot_odds <= 0.700 AND hand_equity <= 0.335 AND position_relative_button > 2.500 AND pot_commitment <= 0.086 AND position_numeric > 1.500 AND stack_to_pot_ratio <= 1.309
**Samples:** 1
**Confidence:** 100.0%

### Rule 7: FOLD
**Conditions:** effective_stack > 33.306 AND pot_odds > 0.288 AND pot_odds <= 0.700 AND hand_equity <= 0.335 AND position_relative_button > 2.500 AND pot_commitment <= 0.086 AND position_numeric > 1.500 AND stack_to_pot_ratio > 1.309 AND hand_equity <= 0.325 AND players_remaining <= 5.500 AND equity_percentile > 33.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 8: FOLD
**Conditions:** effective_stack > 33.306 AND pot_odds > 0.288 AND pot_odds <= 0.700 AND hand_equity <= 0.335 AND position_relative_button > 2.500 AND pot_commitment > 0.086
**Samples:** 1
**Confidence:** 100.0%

### Rule 9: FOLD
**Conditions:** effective_stack > 33.306 AND pot_odds > 0.288 AND pot_odds <= 0.700 AND hand_equity > 0.335 AND players_remaining > 5.500 AND pot_odds > 0.364 AND equity_percentile <= 42.500 AND stack_to_pot_ratio <= 20.833
**Samples:** 1
**Confidence:** 100.0%

### Rule 10: FOLD
**Conditions:** effective_stack > 33.306 AND pot_odds > 0.288 AND pot_odds <= 0.700 AND hand_equity > 0.335 AND players_remaining > 5.500 AND pot_odds > 0.364 AND equity_percentile <= 42.500 AND stack_to_pot_ratio > 20.833
**Samples:** 1
**Confidence:** 100.0%

### Rule 11: CALL
**Conditions:** effective_stack > 33.306 AND pot_odds <= 0.288 AND players_to_act > 4.500 AND is_blind <= 0.500 AND effective_stack > 78.875 AND position_relative_button <= 2.500
**Samples:** 0
**Confidence:** 95.7%

### Rule 12: FOLD
**Conditions:** effective_stack > 33.306 AND pot_odds > 0.288 AND pot_odds <= 0.700 AND hand_equity <= 0.335 AND position_relative_button > 2.500 AND pot_commitment <= 0.086 AND position_numeric <= 1.500 AND equity_percentile > 29.500 AND pot_commitment <= 0.030
**Samples:** 1
**Confidence:** 93.2%

### Rule 13: CALL
**Conditions:** effective_stack > 33.306 AND pot_odds <= 0.288 AND players_to_act > 4.500 AND is_blind <= 0.500 AND effective_stack > 78.875 AND position_relative_button > 2.500 AND position_relative_button > 3.500 AND hand_equity > 0.275 AND equity_percentile <= 31.500
**Samples:** 1
**Confidence:** 92.3%

### Rule 14: CALL
**Conditions:** effective_stack > 33.306 AND pot_odds <= 0.288 AND players_to_act > 4.500 AND is_blind <= 0.500 AND effective_stack > 78.875 AND position_relative_button > 2.500 AND position_relative_button > 3.500 AND hand_equity > 0.275 AND equity_percentile > 31.500 AND equity_percentile > 38.500
**Samples:** 1
**Confidence:** 91.6%

### Rule 15: CALL
**Conditions:** effective_stack > 33.306 AND pot_odds <= 0.288 AND players_to_act <= 4.500 AND position_relative_button > 4.500 AND hand_equity <= 0.405 AND pot_commitment <= 0.156 AND effective_stack > 47.039 AND pot_commitment <= 0.123 AND stack_to_pot_ratio > 2.193 AND pot_size_bb > 11.250
**Samples:** 0
**Confidence:** 89.5%

### Rule 16: FOLD
**Conditions:** effective_stack > 33.306 AND pot_odds > 0.288 AND pot_odds <= 0.700 AND hand_equity > 0.335 AND players_remaining <= 5.500 AND players_to_act > 2.500 AND position_relative_button <= 0.500
**Samples:** 1
**Confidence:** 89.2%

### Rule 17: CALL
**Conditions:** effective_stack > 33.306 AND pot_odds <= 0.288 AND players_to_act <= 4.500 AND position_relative_button <= 4.500 AND pot_size_bb <= 170.972 AND position_relative_button <= 2.500 AND is_blind > 0.500 AND hand_equity <= 0.385 AND pot_size_bb > 3.250 AND pot_size_bb <= 56.521 AND current_bet_bb > 9.773
**Samples:** 1
**Confidence:** 87.7%

### Rule 18: CALL
**Conditions:** effective_stack > 33.306 AND pot_odds <= 0.288 AND players_to_act > 4.500 AND is_blind <= 0.500 AND effective_stack > 78.875 AND position_relative_button > 2.500 AND position_relative_button > 3.500 AND hand_equity > 0.275 AND equity_percentile > 31.500 AND equity_percentile <= 38.500
**Samples:** 1
**Confidence:** 86.0%

### Rule 19: FOLD
**Conditions:** effective_stack > 33.306 AND pot_odds > 0.288 AND pot_odds <= 0.700 AND hand_equity > 0.335 AND players_remaining <= 5.500 AND players_to_act > 2.500 AND position_relative_button > 0.500 AND hand_equity <= 0.385 AND current_bet_bb > 1.250
**Samples:** 0
**Confidence:** 85.8%

### Rule 20: CALL
**Conditions:** effective_stack > 33.306 AND pot_odds <= 0.288 AND players_to_act <= 4.500 AND position_relative_button <= 4.500 AND pot_size_bb <= 170.972 AND position_relative_button > 2.500 AND position_relative_button > 3.500 AND equity_percentile > 29.500 AND pot_odds <= 0.269 AND total_street_bets > 4.500
**Samples:** 0
**Confidence:** 84.6%

## Feature Importance

| Feature | Importance |
|---------|------------|
| effective_stack | 0.566 |
| pot_odds | 0.185 |
| position_relative_button | 0.047 |
| hand_equity | 0.043 |
| players_to_act | 0.035 |
| is_blind | 0.026 |
| equity_percentile | 0.024 |
| pot_commitment | 0.023 |
| pot_size_bb | 0.019 |
| current_bet_bb | 0.011 |
