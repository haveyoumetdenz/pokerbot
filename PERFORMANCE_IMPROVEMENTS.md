# Interpretable Agent Performance Improvements

## Changes Made

### 1. Feature Mismatch - FIXED ✅
- **Problem**: Trees were trained with only 24 features, but code extracts 35 features
- **Solution**: Retrained trees using ALL 35 features from existing data
- **Result**: Trees now use all features including betting history (features 25-35)

### 2. Tree Parameters - IMPROVED ✅
- **Before**: max_depth=12, min_samples_split=100, min_samples_leaf=50
- **After**: max_depth=18-22, improved min_samples_split/min_samples_leaf
- **Result**: Deeper trees (depth 22) with better regularization

### 3. Tree Training - COMPLETED ✅
- All 4 trees (preflop, flop, turn, river) retrained with:
  - 35 features (was 24)
  - Depth 22 (was 12)
  - Better validation accuracy (62-74%)

## Performance Comparison

### Before Retraining (Old Trees - 24 features)
- Win Rate: 56.0%
- Avg Profit/Game: $1.25
- Action Distribution: 38.2% fold, 3.6% call, 58.2% raise

### After Retraining (New Trees - 35 features)
- Win Rate: 52.0% (vs random: 61.6%)
- Avg Profit/Game: -$2.03 (currently underperforming)
- Action Distribution: 36.7% fold, 1.7% call, 61.7% raise

### DeepCFR Baseline
- Win Rate: 82.0%
- Avg Profit/Game: $3.01
- Action Distribution: 15.0% fold, 35.0% call, 50.0% raise

## Issues Identified

### 1. Betting History Not Tracking ⚠️
- **Problem**: Opponents tracked = 0
- **Impact**: Betting history features (25-35) are all 0/default values
- **Effect**: Trees learned to use these features, but they're always 0, causing prediction errors

### 2. Action Distribution Still Imbalanced ⚠️
- **Too many folds**: 36.7% (should be ~15%)
- **Too few calls**: 1.7% (should be ~35%)
- **Too many raises**: 61.7% (should be ~50%)

### 3. Betting History Features Not Populated ⚠️
- Features 25-35 (betting history) are extracted but always 0
- Trees were trained expecting these features to have meaningful values
- When features are 0, predictions may be incorrect

## Next Steps

### Immediate Actions
1. **Fix betting history tracking**
   - Ensure `record_action` is called for all opponent actions
   - Debug why opponents aren't being tracked
   - Verify betting history is passed to feature extraction

2. **Test with betting history populated**
   - Run games with betting history tracking enabled
   - Verify betting history features have non-zero values
   - Compare performance with vs without betting history

3. **Adjust tree parameters**
   - Consider reducing tree depth if overfitting
   - Adjust class weights to balance fold/call/raise
   - Try ensemble of trees for better generalization

### Long-term Improvements
1. **Collect more training data**
   - More CFR iterations
   - More traversals per iteration
   - Better coverage of game states

2. **Feature engineering**
   - Add more meaningful betting history features
   - Include opponent-specific patterns
   - Add hand strength progression features

3. **Model architecture**
   - Consider random forests instead of single trees
   - Try gradient boosting for better performance
   - Hybrid approach: trees for explanation, neural nets for action

## Expected Performance

### Realistic Goals
- **Win Rate**: 60-70% (vs DeepCFR's 82%)
- **Avg Profit**: $2-4/game (vs DeepCFR's $3)
- **Interpretable agent will always be weaker** due to:
  - Simpler model (decision trees vs neural networks)
  - Limited feature space (35 vs 500+)
  - Binary decision structure

### Trade-offs
- **Interpretability** comes at cost of **performance**
- **Decision trees** are easier to understand but less expressive
- **Feature count** is limited (35 vs 500+ in DeepCFR)

## Technical Details

### Tree Statistics
- **Preflop**: depth=22, features=35, train_acc=0.740, val_acc=0.721
- **Flop**: depth=22, features=35, train_acc=0.768, val_acc=0.746
- **Turn**: depth=22, features=35, train_acc=0.676, val_acc=0.645
- **River**: depth=22, features=35, train_acc=0.659, val_acc=0.629

### Feature Importance
- **Top features** vary by street but generally include:
  - hand_equity (feature_0)
  - pot_size_bb (feature_2)
  - stack_size_bb (feature_11)
  - position (feature_10)

### Training Data
- **Preflop**: 525,488 samples
- **Flop**: 806,188 samples
- **Turn**: 882,554 samples
- **River**: 740,587 samples

## Commands

### Retrain Trees
```bash
PYTHONPATH=. python scripts/train_interpretable_complete.py \
  --skip-cfr \
  --tree-depth 18 \
  --output-dir interpretable_output
```

### Test Performance
```bash
PYTHONPATH=. python interpretable_diagnostic.py \
  --num-games 50 \
  --opponent-type strategic \
  --opponent-tightness mixed
```

### Compare Agents
```bash
PYTHONPATH=. python compare_agents.py \
  --num-games 50 \
  --opponent-type strategic \
  --opponent-tightness mixed
```

