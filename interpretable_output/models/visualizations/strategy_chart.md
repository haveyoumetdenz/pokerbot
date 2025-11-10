# Poker Strategy Chart - Interpretable AI

## Overview
This chart summarizes the strategy learned by the interpretable poker AI across all betting rounds.

## Opening Ranges by Position

### Preflop Strategy
#### Early Position
- Tight range: Premium hands only
- Fold most hands, raise with strong hands

#### Middle Position
- Moderate range: Good hands and some speculative hands
- Call with medium strength, raise with strong hands

#### Late Position
- Wide range: Can play more hands due to position
- Steal blinds with weaker hands

### Flop Strategy
#### Key Factors
- Hand equity is the primary factor
- Pot odds determine calling decisions
- Position affects betting frequency

### Turn Strategy
#### Key Factors
- Hand equity is the primary factor
- Pot odds determine calling decisions
- Position affects betting frequency

### River Strategy
#### Key Factors
- Hand equity is the primary factor
- Pot odds determine calling decisions
- Position affects betting frequency

## General Principles

### Value Betting
- Bet for value when you have a strong hand
- Size bets to get called by weaker hands
- Consider opponent's likely range

### Bluffing
- Bluff when you have fold equity
- Use position to your advantage
- Consider pot odds and stack sizes

### Pot Odds
- Call when pot odds are favorable
- Fold when pot odds are unfavorable
- Consider implied odds for future streets

## Feature Importance Summary

The AI considers these factors in order of importance:
1. Hand equity - Probability of winning
2. Pot odds - Ratio of pot to call amount
3. Position - Table position relative to button
4. Stack size - Effective stack size
5. Betting history - Previous actions this street

## Decision Tree Statistics

### Preflop
- Tree depth: 12
- Number of leaves: 2509
- Features used: 24

### Flop
- Tree depth: 12
- Number of leaves: 2531
- Features used: 24

### Turn
- Tree depth: 6
- Number of leaves: 64
- Features used: 24

### River
- Tree depth: 12
- Number of leaves: 2417
- Features used: 24

