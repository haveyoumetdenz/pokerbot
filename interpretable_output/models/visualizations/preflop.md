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

### Rule 1: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button <= 0.500 AND players_remaining <= 2.500 AND current_bet_bb <= 34.643 AND pot_commitment <= 0.032 AND pot_size_bb <= 101.750 AND hand_equity <= 0.325
**Samples:** 1
**Confidence:** 100.0%

### Rule 2: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button <= 0.500 AND players_remaining <= 2.500 AND current_bet_bb <= 34.643 AND pot_commitment <= 0.032 AND pot_size_bb > 101.750 AND hand_equity <= 0.275 AND stack_to_pot_ratio > 0.923
**Samples:** 1
**Confidence:** 100.0%

### Rule 3: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button <= 0.500 AND players_remaining <= 2.500 AND current_bet_bb <= 34.643 AND pot_commitment <= 0.032 AND pot_size_bb > 101.750 AND hand_equity > 0.275 AND stack_size_bb <= 96.560
**Samples:** 1
**Confidence:** 100.0%

### Rule 4: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button <= 0.500 AND players_remaining <= 2.500 AND current_bet_bb <= 34.643 AND pot_commitment <= 0.032 AND pot_size_bb > 101.750 AND hand_equity > 0.275 AND stack_size_bb > 96.560
**Samples:** 1
**Confidence:** 100.0%

### Rule 5: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button <= 0.500 AND players_remaining <= 2.500 AND current_bet_bb > 34.643 AND pot_odds <= 0.230 AND pot_size_bb <= 144.365 AND stack_to_pot_ratio > 0.442 AND effective_stack <= 26.721
**Samples:** 1
**Confidence:** 100.0%

### Rule 6: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button <= 0.500 AND players_remaining <= 2.500 AND current_bet_bb > 34.643 AND pot_odds <= 0.230 AND pot_size_bb <= 144.365 AND stack_to_pot_ratio > 0.442 AND effective_stack > 26.721
**Samples:** 1
**Confidence:** 100.0%

### Rule 7: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button <= 0.500 AND players_remaining <= 2.500 AND current_bet_bb > 34.643 AND pot_odds <= 0.230 AND pot_size_bb > 144.365 AND effective_stack <= 3.419
**Samples:** 1
**Confidence:** 100.0%

### Rule 8: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button <= 0.500 AND players_remaining <= 2.500 AND current_bet_bb > 34.643 AND pot_odds <= 0.230 AND pot_size_bb > 144.365 AND effective_stack > 3.419
**Samples:** 1
**Confidence:** 100.0%

### Rule 9: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button <= 0.500 AND players_remaining <= 2.500 AND current_bet_bb > 34.643 AND pot_odds > 0.230 AND stack_size_bb <= 56.723 AND pot_odds <= 0.239 AND pot_size_bb <= 149.752
**Samples:** 1
**Confidence:** 100.0%

### Rule 10: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button <= 0.500 AND players_remaining > 2.500 AND effective_stack > 20.016 AND pot_size_bb <= 151.961 AND stack_size_bb <= 65.865 AND hand_equity > 0.365
**Samples:** 1
**Confidence:** 100.0%

### Rule 11: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button > 0.500 AND stack_to_pot_ratio <= 0.458 AND stack_to_pot_ratio <= 0.323 AND players_remaining <= 2.500 AND pot_commitment <= 0.304
**Samples:** 1
**Confidence:** 100.0%

### Rule 12: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button > 0.500 AND stack_to_pot_ratio <= 0.458 AND stack_to_pot_ratio > 0.323 AND pot_odds <= 0.311 AND stack_to_pot_ratio <= 0.367 AND hand_equity > 0.385 AND stack_to_pot_ratio <= 0.362
**Samples:** 1
**Confidence:** 100.0%

### Rule 13: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button > 0.500 AND stack_to_pot_ratio <= 0.458 AND stack_to_pot_ratio > 0.323 AND pot_odds > 0.311 AND pot_commitment > 0.129 AND equity_percentile > 31.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 14: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button > 0.500 AND stack_to_pot_ratio > 0.458 AND pot_size_bb <= 109.818 AND players_to_act <= 2.500 AND pot_size_bb > 106.085 AND stack_to_pot_ratio > 0.916 AND stack_size_bb > 98.750
**Samples:** 1
**Confidence:** 100.0%

### Rule 15: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button > 0.500 AND stack_to_pot_ratio > 0.458 AND pot_size_bb <= 109.818 AND players_to_act > 2.500 AND pot_size_bb > 106.125 AND hand_equity > 0.305 AND equity_percentile <= 39.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 16: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button > 0.500 AND stack_to_pot_ratio > 0.458 AND pot_size_bb > 109.818 AND effective_stack <= 15.998 AND total_street_bets > 3.500 AND hand_equity <= 0.245
**Samples:** 1
**Confidence:** 100.0%

### Rule 17: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack <= 41.300 AND position_relative_button > 0.500 AND stack_to_pot_ratio > 0.458 AND pot_size_bb > 109.818 AND effective_stack > 15.998 AND pot_odds <= 0.187 AND current_bet_bb <= 30.161 AND stack_size_bb <= 73.847
**Samples:** 1
**Confidence:** 100.0%

### Rule 18: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack > 41.300 AND pot_commitment <= 0.198 AND pot_odds <= 0.392 AND is_button <= 0.500 AND pot_commitment > 0.115 AND pot_odds > 0.299 AND pot_size_bb <= 43.312 AND pot_commitment <= 0.166
**Samples:** 1
**Confidence:** 100.0%

### Rule 19: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack > 41.300 AND pot_commitment <= 0.198 AND pot_odds <= 0.392 AND is_button > 0.500 AND players_to_act <= 2.500 AND current_bet_bb > 6.548 AND effective_stack > 84.982 AND pot_size_bb > 40.750
**Samples:** 1
**Confidence:** 100.0%

### Rule 20: CALL
**Conditions:** pot_size_bb <= 188.545 AND position_relative_button <= 1.500 AND players_remaining <= 5.500 AND players_remaining <= 4.500 AND effective_stack > 41.300 AND pot_commitment <= 0.198 AND pot_odds > 0.392
**Samples:** 1
**Confidence:** 100.0%

## Feature Importance

| Feature | Importance |
|---------|------------|
| pot_size_bb | 0.597 |
| position_relative_button | 0.127 |
| effective_stack | 0.098 |
| players_to_act | 0.037 |
| players_remaining | 0.030 |
| position_numeric | 0.024 |
| pot_odds | 0.019 |
| stack_size_bb | 0.017 |
| stack_to_pot_ratio | 0.014 |
| pot_commitment | 0.011 |
