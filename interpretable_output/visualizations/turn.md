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
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity <= 0.195
**Samples:** 1
**Confidence:** 100.0%

### Rule 2: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile <= 21.500 AND pot_size_bb <= 209.375 AND hand_equity <= 0.385 AND hand_equity <= 0.285 AND equity_percentile <= 20.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 3: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile <= 21.500 AND pot_size_bb <= 209.375 AND hand_equity <= 0.385 AND hand_equity > 0.285 AND hand_equity > 0.295 AND pot_size_bb > 207.250
**Samples:** 1
**Confidence:** 100.0%

### Rule 4: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile <= 21.500 AND pot_size_bb <= 209.375 AND hand_equity > 0.385 AND equity_percentile <= 20.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 5: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile <= 21.500 AND pot_size_bb > 209.375 AND hand_equity <= 0.335 AND pot_size_bb <= 213.457
**Samples:** 1
**Confidence:** 100.0%

### Rule 6: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile <= 21.500 AND pot_size_bb > 209.375 AND hand_equity > 0.335 AND hand_equity <= 0.355
**Samples:** 1
**Confidence:** 100.0%

### Rule 7: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile <= 21.500 AND pot_size_bb > 209.375 AND hand_equity > 0.335 AND hand_equity > 0.355
**Samples:** 1
**Confidence:** 100.0%

### Rule 8: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile > 21.500 AND pot_size_bb <= 214.962 AND pot_size_bb <= 214.213 AND pot_size_bb <= 213.984 AND equity_percentile <= 37.500 AND pot_size_bb > 213.656
**Samples:** 1
**Confidence:** 100.0%

### Rule 9: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile > 21.500 AND pot_size_bb <= 214.962 AND pot_size_bb <= 214.213 AND pot_size_bb <= 213.984 AND equity_percentile > 37.500 AND equity_percentile <= 39.500 AND pot_size_bb > 212.185 AND pot_size_bb <= 212.950
**Samples:** 1
**Confidence:** 100.0%

### Rule 10: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile > 21.500 AND pot_size_bb <= 214.962 AND pot_size_bb <= 214.213 AND pot_size_bb <= 213.984 AND equity_percentile > 37.500 AND equity_percentile > 39.500 AND pot_size_bb > 211.562 AND pot_size_bb <= 212.736
**Samples:** 1
**Confidence:** 100.0%

### Rule 11: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile > 21.500 AND pot_size_bb <= 214.962 AND pot_size_bb <= 214.213 AND pot_size_bb > 213.984 AND equity_percentile > 34.500 AND hand_equity > 0.345
**Samples:** 1
**Confidence:** 100.0%

### Rule 12: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile > 21.500 AND pot_size_bb <= 214.962 AND pot_size_bb > 214.213 AND equity_percentile <= 37.500 AND equity_percentile <= 29.500 AND equity_percentile <= 27.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 13: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile > 21.500 AND pot_size_bb <= 214.962 AND pot_size_bb > 214.213 AND equity_percentile <= 37.500 AND equity_percentile > 29.500 AND hand_equity <= 0.305
**Samples:** 1
**Confidence:** 100.0%

### Rule 14: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile > 21.500 AND pot_size_bb <= 214.962 AND pot_size_bb > 214.213 AND equity_percentile <= 37.500 AND equity_percentile > 29.500 AND hand_equity > 0.305
**Samples:** 1
**Confidence:** 100.0%

### Rule 15: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile > 21.500 AND pot_size_bb > 214.962 AND hand_equity <= 0.255
**Samples:** 1
**Confidence:** 100.0%

### Rule 16: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile > 21.500 AND pot_size_bb > 214.962 AND hand_equity > 0.255 AND equity_percentile <= 39.500 AND pot_size_bb > 215.062 AND pot_size_bb <= 215.450
**Samples:** 1
**Confidence:** 100.0%

### Rule 17: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile > 21.500 AND pot_size_bb > 214.962 AND hand_equity > 0.255 AND equity_percentile <= 39.500 AND pot_size_bb > 215.062 AND pot_size_bb > 215.450 AND equity_percentile <= 33.500 AND equity_percentile > 32.500
**Samples:** 1
**Confidence:** 100.0%

### Rule 18: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile > 21.500 AND pot_size_bb > 214.962 AND hand_equity > 0.255 AND equity_percentile <= 39.500 AND pot_size_bb > 215.062 AND pot_size_bb > 215.450 AND equity_percentile > 33.500 AND pot_size_bb <= 215.552
**Samples:** 1
**Confidence:** 100.0%

### Rule 19: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile > 21.500 AND pot_size_bb > 214.962 AND hand_equity > 0.255 AND equity_percentile > 39.500 AND pot_size_bb > 215.569 AND pot_size_bb <= 216.121
**Samples:** 1
**Confidence:** 100.0%

### Rule 20: FOLD
**Conditions:** effective_stack <= 0.499 AND pot_size_bb <= 334.940 AND stack_size_bb <= 0.608 AND pot_size_bb <= 257.664 AND fold_equity <= 0.150 AND pot_size_bb <= 217.436 AND position_relative_button <= 2.500 AND pot_size_bb > 200.250 AND stack_size_bb <= 0.338 AND pot_size_bb <= 217.022 AND hand_equity > 0.195 AND equity_percentile <= 43.500 AND pot_size_bb <= 216.726 AND pot_size_bb <= 216.574 AND equity_percentile > 21.500 AND pot_size_bb > 214.962 AND hand_equity > 0.255 AND equity_percentile > 39.500 AND pot_size_bb > 215.569 AND pot_size_bb > 216.121
**Samples:** 1
**Confidence:** 100.0%

## Feature Importance

| Feature | Importance |
|---------|------------|
| effective_stack | 0.555 |
| pot_size_bb | 0.215 |
| stack_size_bb | 0.080 |
| equity_percentile | 0.046 |
| hand_equity | 0.042 |
| stack_to_pot_ratio | 0.022 |
| position_relative_button | 0.012 |
| total_street_bets | 0.006 |
| pot_odds | 0.005 |
| players_remaining | 0.004 |
