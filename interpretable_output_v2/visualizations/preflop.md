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
**Conditions:** effective_stack <= 44.000 AND current_bet_bb <= 40.658 AND stack_to_pot_ratio <= 0.332 AND players_to_act <= 3.500 AND stack_to_pot_ratio <= 0.254 AND stack_to_pot_ratio <= 0.201 AND pot_commitment <= 0.086 AND pot_size_bb <= 362.805
**Samples:** 1
**Confidence:** 100.0%

### Rule 2: FOLD
**Conditions:** effective_stack <= 44.000 AND current_bet_bb > 40.658 AND stack_to_pot_ratio <= 0.185 AND current_bet_bb <= 54.117 AND effective_stack <= 24.998 AND stack_size_bb > 52.744 AND stack_to_pot_ratio > 0.184
**Samples:** 1
**Confidence:** 100.0%

### Rule 3: RAISE
**Conditions:** effective_stack <= 44.000 AND current_bet_bb > 40.658 AND stack_to_pot_ratio <= 0.185 AND current_bet_bb <= 54.117 AND effective_stack > 24.998 AND pot_size_bb <= 275.176
**Samples:** 1
**Confidence:** 100.0%

### Rule 4: RAISE
**Conditions:** effective_stack <= 44.000 AND current_bet_bb > 40.658 AND stack_to_pot_ratio <= 0.185 AND current_bet_bb <= 54.117 AND effective_stack > 24.998 AND pot_size_bb > 275.176 AND current_bet_bb > 46.643 AND equity_percentile <= 21.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 5: RAISE
**Conditions:** effective_stack <= 44.000 AND current_bet_bb > 40.658 AND stack_to_pot_ratio > 0.185 AND stack_to_pot_ratio <= 0.255 AND effective_stack > 24.995 AND stack_to_pot_ratio <= 0.235 AND pot_size_bb <= 220.720
**Samples:** 1
**Confidence:** 100.0%

### Rule 6: RAISE
**Conditions:** effective_stack <= 44.000 AND current_bet_bb > 40.658 AND stack_to_pot_ratio > 0.185 AND stack_to_pot_ratio <= 0.255 AND effective_stack > 24.995 AND stack_to_pot_ratio > 0.235 AND pot_size_bb <= 211.727
**Samples:** 1
**Confidence:** 100.0%

### Rule 7: RAISE
**Conditions:** effective_stack <= 44.000 AND current_bet_bb > 40.658 AND stack_to_pot_ratio > 0.185 AND stack_to_pot_ratio > 0.255 AND pot_odds <= 0.131 AND pot_size_bb <= 187.868
**Samples:** 1
**Confidence:** 100.0%

### Rule 8: RAISE
**Conditions:** effective_stack <= 44.000 AND current_bet_bb > 40.658 AND stack_to_pot_ratio > 0.185 AND stack_to_pot_ratio > 0.255 AND pot_odds <= 0.131 AND pot_size_bb > 187.868 AND pot_size_bb > 189.438 AND stack_to_pot_ratio > 0.298
**Samples:** 1
**Confidence:** 100.0%

### Rule 9: RAISE
**Conditions:** effective_stack > 44.000 AND players_to_act <= 4.500 AND effective_stack <= 48.195 AND stack_size_bb <= 91.003 AND stack_to_pot_ratio <= 0.548 AND pot_size_bb > 204.169 AND equity_percentile <= 25.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 10: RAISE
**Conditions:** effective_stack > 44.000 AND players_to_act <= 4.500 AND effective_stack <= 48.195 AND stack_size_bb <= 91.003 AND stack_to_pot_ratio <= 0.548 AND pot_size_bb > 204.169 AND equity_percentile > 25.500 AND pot_commitment > 0.162
**Samples:** 1
**Confidence:** 100.0%

### Rule 11: FOLD
**Conditions:** effective_stack > 44.000 AND players_to_act <= 4.500 AND effective_stack <= 48.195 AND stack_size_bb > 91.003 AND effective_stack <= 46.501 AND hand_equity > 0.255 AND pot_commitment <= 0.016 AND pot_odds > 0.273
**Samples:** 1
**Confidence:** 100.0%

### Rule 12: RAISE
**Conditions:** effective_stack > 44.000 AND players_to_act <= 4.500 AND effective_stack <= 48.195 AND stack_size_bb > 91.003 AND effective_stack > 46.501 AND stack_size_bb <= 95.140 AND effective_stack <= 46.561 AND pot_size_bb <= 97.159
**Samples:** 1
**Confidence:** 100.0%

### Rule 13: RAISE
**Conditions:** effective_stack > 44.000 AND players_to_act <= 4.500 AND effective_stack > 48.195 AND total_street_bets <= 4.500 AND pot_size_bb > 120.321 AND current_bet_bb > 34.021 AND equity_percentile <= 31.500 AND hand_equity <= 0.295
**Samples:** 1
**Confidence:** 100.0%

### Rule 14: RAISE
**Conditions:** effective_stack > 44.000 AND players_to_act <= 4.500 AND effective_stack > 48.195 AND total_street_bets <= 4.500 AND pot_size_bb > 120.321 AND current_bet_bb > 34.021 AND equity_percentile > 31.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 15: RAISE
**Conditions:** effective_stack > 44.000 AND players_to_act > 4.500 AND effective_stack <= 48.180 AND stack_size_bb <= 91.130 AND stack_size_bb <= 86.075
**Samples:** 1
**Confidence:** 100.0%

### Rule 16: RAISE
**Conditions:** effective_stack > 44.000 AND players_to_act > 4.500 AND effective_stack <= 48.180 AND stack_size_bb <= 91.130 AND stack_size_bb > 86.075 AND current_bet_bb <= 10.240 AND effective_stack > 45.757
**Samples:** 1
**Confidence:** 100.0%

### Rule 17: RAISE
**Conditions:** effective_stack > 44.000 AND players_to_act > 4.500 AND effective_stack <= 48.180 AND stack_size_bb <= 91.130 AND stack_size_bb > 86.075 AND current_bet_bb > 10.240 AND effective_stack <= 44.716
**Samples:** 1
**Confidence:** 100.0%

### Rule 18: FOLD
**Conditions:** effective_stack > 44.000 AND players_to_act > 4.500 AND effective_stack <= 48.180 AND stack_size_bb > 91.130 AND effective_stack <= 45.807 AND equity_percentile <= 28.500 AND effective_stack > 45.046 AND pot_odds <= 0.202
**Samples:** 1
**Confidence:** 100.0%

### Rule 19: FOLD
**Conditions:** effective_stack > 44.000 AND players_to_act > 4.500 AND effective_stack <= 48.180 AND stack_size_bb > 91.130 AND effective_stack <= 45.807 AND equity_percentile <= 28.500 AND effective_stack > 45.046 AND pot_odds > 0.202
**Samples:** 1
**Confidence:** 100.0%

### Rule 20: FOLD
**Conditions:** effective_stack > 44.000 AND players_to_act > 4.500 AND effective_stack <= 48.180 AND stack_size_bb > 91.130 AND effective_stack <= 45.807 AND equity_percentile > 28.500 AND is_blind <= 0.500
**Samples:** 1
**Confidence:** 100.0%

## Feature Importance

| Feature | Importance |
|---------|------------|
| effective_stack | 0.717 |
| current_bet_bb | 0.161 |
| stack_to_pot_ratio | 0.056 |
| players_to_act | 0.011 |
| players_remaining | 0.011 |
| hand_equity | 0.008 |
| pot_size_bb | 0.007 |
| pot_odds | 0.007 |
| stack_size_bb | 0.007 |
| pot_commitment | 0.007 |
