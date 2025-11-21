# Interpretable Agent "Always Raising" Issue - Analysis & Fix

## Problem
The interpretable agent showed 100% raise actions (0 folds, 0 calls, 284 raises) in evaluation against strategic opponents.

## Root Causes Identified

### 1. **Preflop Tree Missing 'Fold' Class**
- The preflop decision tree only has 2 classes: `['call', 'raise']`
- No 'fold' class exists, so the tree cannot predict folds preflop
- **Training data**: Preflop had 60.7% raises, 39.3% calls, 0% folds

### 2. **Training Data Imbalance**
- **Preflop**: 60.7% raise, 39.3% call, 0% fold
- **Flop**: 46.4% fold, 38.3% raise, 15.3% call
- **Turn**: 60.9% fold, 30.7% raise, 8.5% call
- **River**: 65.1% fold, 28.4% raise, 6.5% call

The trees learned this distribution, so they predict 'raise' more often than 'fold' or 'call' in many situations.

### 3. **Missing Legal Action Validation**
- The `_category_to_action` method didn't check if the predicted action was legal
- If the tree predicted an illegal action, it would still try to execute it
- This could cause unexpected behavior or fallbacks

## Fixes Applied

### 1. **Legal Action Validation** ✅
Updated `_category_to_action` to:
- Check if predicted action is legal before executing
- Fallback to legal alternatives if predicted action is illegal
- Priority: Call/Check > Fold > Raise (as last resort)

### 2. **Diagnostic Script** ✅
Created `scripts/diagnose_interpretable.py` to:
- Check tree predictions on random inputs
- Verify training data distribution
- Test action conversion logic
- Test agent decisions on sample game states

## Test Results

### Against Random Opponents
- **Action Distribution**: 63.1% raise, 22.0% call, 14.9% fold
- **Tree Predictions**: Match action distribution (no conversion issues)

### Against Strategic Opponents (from evaluation)
- **Action Distribution**: 0% fold, 0% call, 100% raise (284 raises)
- This suggests the trees predict 'raise' more often against strategic opponents

## Why 100% Raises Against Strategic Opponents?

Possible explanations:
1. **Context-dependent predictions**: Against strategic opponents, game states might favor raising
2. **Training bias**: Trees were trained on data where raising was profitable (60%+ in preflop)
3. **Missing fold data**: Preflop tree has no fold class, so it can't fold preflop
4. **Strategic opponent behavior**: Strategic opponents might create game states where the trees predict 'raise' as optimal

## Recommendations

### Short-term
1. ✅ **Legal action validation** - Already fixed
2. **Retrain with more balanced data** - Collect more fold/call examples during DeepCFR training
3. **Check evaluation context** - Verify if strategic opponents create different game states

### Long-term
1. **Progressive training** - Train DeepCFR against random → strategic → mixed opponents
2. **Balanced data collection** - Ensure all action types are well-represented in training data
3. **Tree regularization** - Use class weights or sampling to balance tree training

## Next Steps

1. Run evaluation again with the legal action validation fix
2. Check if action distribution improves
3. If still 100% raises, investigate:
   - Are trees actually predicting 'raise' 100% of the time?
   - Or is there a bug in action counting?
   - Are strategic opponents creating game states that favor raising?


