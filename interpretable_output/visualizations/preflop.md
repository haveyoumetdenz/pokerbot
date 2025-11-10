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
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile <= 29.500 AND pot_odds <= 0.146 AND pot_odds <= 0.125 AND pot_odds <= 0.095 AND pot_commitment <= 0.196
**Samples:** 1
**Confidence:** 100.0%

### Rule 2: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile <= 29.500 AND pot_odds <= 0.146 AND pot_odds <= 0.125 AND pot_odds <= 0.095 AND pot_commitment > 0.196 AND hand_equity <= 0.305
**Samples:** 1
**Confidence:** 100.0%

### Rule 3: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile <= 29.500 AND pot_odds <= 0.146 AND pot_odds <= 0.125 AND pot_odds > 0.095 AND equity_percentile > 21.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 4: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile <= 29.500 AND pot_odds <= 0.146 AND pot_odds > 0.125 AND effective_stack <= 33.436
**Samples:** 1
**Confidence:** 100.0%

### Rule 5: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile <= 29.500 AND pot_odds <= 0.146 AND pot_odds > 0.125 AND effective_stack > 33.436 AND hand_equity <= 0.335 AND hand_equity <= 0.305 AND hand_equity > 0.275
**Samples:** 1
**Confidence:** 100.0%

### Rule 6: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile <= 29.500 AND pot_odds <= 0.146 AND pot_odds > 0.125 AND effective_stack > 33.436 AND hand_equity > 0.335
**Samples:** 1
**Confidence:** 100.0%

### Rule 7: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile <= 29.500 AND pot_odds > 0.146
**Samples:** 1
**Confidence:** 100.0%

### Rule 8: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile > 29.500 AND effective_stack <= 13.153 AND stack_to_pot_ratio <= 0.304
**Samples:** 1
**Confidence:** 100.0%

### Rule 9: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile > 29.500 AND effective_stack <= 13.153 AND stack_to_pot_ratio > 0.304 AND hand_equity <= 0.315
**Samples:** 1
**Confidence:** 100.0%

### Rule 10: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile > 29.500 AND effective_stack <= 13.153 AND stack_to_pot_ratio > 0.304 AND hand_equity > 0.315 AND position_relative_button <= 2.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 11: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile > 29.500 AND effective_stack <= 13.153 AND stack_to_pot_ratio > 0.304 AND hand_equity > 0.315 AND position_relative_button > 2.500 AND pot_size_bb <= 185.698
**Samples:** 1
**Confidence:** 100.0%

### Rule 12: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile > 29.500 AND effective_stack <= 13.153 AND stack_to_pot_ratio > 0.304 AND hand_equity > 0.315 AND position_relative_button > 2.500 AND pot_size_bb > 185.698 AND effective_stack <= 2.224 AND pot_odds <= 0.260
**Samples:** 1
**Confidence:** 100.0%

### Rule 13: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile > 29.500 AND effective_stack > 13.153 AND effective_stack <= 33.726 AND stack_size_bb <= 48.678
**Samples:** 1
**Confidence:** 100.0%

### Rule 14: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile > 29.500 AND effective_stack > 13.153 AND effective_stack <= 33.726 AND stack_size_bb > 48.678
**Samples:** 1
**Confidence:** 100.0%

### Rule 15: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile > 29.500 AND effective_stack > 13.153 AND effective_stack > 33.726 AND pot_size_bb <= 219.666 AND total_street_bets <= 4.500 AND pot_commitment <= 0.211 AND fold_equity <= 0.150 AND current_bet_bb > 30.042
**Samples:** 1
**Confidence:** 100.0%

### Rule 16: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile > 29.500 AND effective_stack > 13.153 AND effective_stack > 33.726 AND pot_size_bb <= 219.666 AND total_street_bets <= 4.500 AND pot_commitment > 0.211
**Samples:** 1
**Confidence:** 100.0%

### Rule 17: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile > 29.500 AND effective_stack > 13.153 AND effective_stack > 33.726 AND pot_size_bb <= 219.666 AND total_street_bets > 4.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 18: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile <= 31.500 AND equity_percentile > 29.500 AND effective_stack > 13.153 AND effective_stack > 33.726 AND pot_size_bb > 219.666
**Samples:** 1
**Confidence:** 100.0%

### Rule 19: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile > 31.500 AND effective_stack <= 33.590 AND pot_odds <= 0.099 AND stack_to_pot_ratio <= 0.240 AND position_numeric <= 1.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 20: FOLD
**Conditions:** stack_to_pot_ratio <= 0.357 AND pot_size_bb <= 236.007 AND equity_percentile > 31.500 AND effective_stack <= 33.590 AND pot_odds <= 0.099 AND stack_to_pot_ratio <= 0.240 AND position_numeric > 1.500
**Samples:** 1
**Confidence:** 100.0%

## Feature Importance

| Feature | Importance |
|---------|------------|
| stack_to_pot_ratio | 0.509 |
| pot_size_bb | 0.196 |
| effective_stack | 0.115 |
| equity_percentile | 0.049 |
| current_bet_bb | 0.027 |
| hand_equity | 0.022 |
| pot_odds | 0.020 |
| pot_commitment | 0.017 |
| players_to_act | 0.015 |
| position_relative_button | 0.012 |
