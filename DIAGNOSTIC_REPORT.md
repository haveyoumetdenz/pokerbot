# Interpretable Agent Diagnostic Report

## Test Configuration
- **Games**: 50 per agent
- **Opponents**: Strategic agents with mixed tightness levels
  - Very Tight, Tight, Average, Loose, Very Loose
- **Test Date**: 2024-10-22

---

## Overall Performance Comparison

| Metric | DeepCFR | Interpretable | Difference |
|--------|---------|---------------|------------|
| **Win Rate** | 86.0% | 56.0% | **-30.0%** |
| **Total Profit** | $384.13 | $62.69 | **-$321.44** |
| **Avg Profit/Game** | $7.68 | $1.25 | **-$6.43** |
| **Wins** | 43 | 28 | **-15** |
| **Total Actions** | 60 | 55 | -5 |

### Key Findings
- **Interpretable agent underperforms by 512.8%** in average profit per game
- **Win rate is 30 percentage points lower** than DeepCFR
- Interpretable agent is **significantly less profitable** overall

---

## Action Distribution Analysis

| Action | DeepCFR | Interpretable | Difference |
|--------|---------|---------------|------------|
| **FOLD** | 11.7% | 38.2% | **+26.5%** |
| **CALL** | 28.3% | 3.6% | **-24.7%** |
| **RAISE** | 60.0% | 58.2% | -1.8% |

### Key Issues
1. **Interpretable agent folds too often** (38.2% vs 11.7%)
2. **Interpretable agent rarely calls** (3.6% vs 28.3%)
3. **Action distribution is imbalanced** - too aggressive or too passive

---

## Performance by Street (Interpretable Agent)

| Street | Folds | Calls | Raises | Total |
|--------|-------|-------|--------|-------|
| **Preflop** | 21 (43.8%) | 2 (4.2%) | 25 (52.1%) | 48 |
| **Flop** | 0 (0.0%) | 0 (0.0%) | 5 (100.0%) | 5 |
| **Turn** | 0 (0.0%) | 0 (0.0%) | 1 (100.0%) | 1 |
| **River** | 0 (0.0%) | 0 (0.0%) | 1 (100.0%) | 1 |

### Observations
- **Preflop**: Most folds happen here (43.8% of preflop actions)
- **Post-flop**: Agent is extremely aggressive (100% raises on flop/turn/river)
- **No calls post-flop**: Agent only raises or folds

---

## Decision Quality Analysis (Interpretable Agent)

- **High Equity Folds (>60% equity)**: 0 ✅
- **High Equity Raises (>60% equity)**: 0 ⚠️
- **Low Equity Calls (<30% equity)**: 1 ✅

### Assessment
- **No high-equity folds detected** - Good! Agent doesn't fold strong hands
- **No high-equity raises detected** - Problem! This might indicate:
  - Equity calculation issues
  - Tree predictions not reflecting equity properly
  - Limited sample size

---

## Betting History Status

- **Games Played**: 51
- **Opponents Tracked**: 0 ⚠️
- **Street-Level Statistics**: Not available

### Issues
- **Opponents are not being tracked** despite betting history implementation
- **Street-level statistics not populated** - may indicate:
  - `record_action` not being called properly
  - Exceptions being silently caught
  - Betting history features not being used by trees

---

## Root Cause Analysis

### 1. Feature Count Mismatch
- **Current trees trained with**: 24 features
- **Code extracts**: 35 features (including betting history)
- **Trees only use first 24 features** - betting history features ignored

### 2. Tree Training Data
- Trees were trained **before betting history features were added**
- Betting history features will be 0/default values until trees are retrained

### 3. Action Distribution Imbalance
- **Too many folds** - trees may be too conservative
- **Too few calls** - trees prefer binary decisions (fold/raise)
- **Decision trees struggle with nuanced decisions** compared to neural networks

### 4. Limited Decision Quality
- **No high-equity raises detected** suggests:
  - Equity might not be properly calculated in diagnostic
  - Trees might not be using equity effectively
  - Sample size may be too small

---

## Recommendations

### Immediate Actions
1. **Retrain trees with betting history features**
   ```bash
   PYTHONPATH=. python scripts/train_interpretable_complete.py \
     --skip-cfr \
     --tree-depth 15 \
     --output-dir interpretable_output
   ```

2. **Fix betting history tracking**
   - Debug why opponents aren't being tracked
   - Ensure `record_action` is called for all opponent actions
   - Verify exceptions aren't being silently caught

3. **Tune tree parameters**
   - Increase tree depth (currently 15 recommended)
   - Adjust min_samples_split to reduce over-folding
   - Consider ensemble of trees for better generalization

### Long-term Improvements
1. **Collect more training data**
   - More CFR iterations
   - More traversals per iteration
   - Better coverage of game states

2. **Feature engineering**
   - Add more betting history features
   - Include opponent-specific features
   - Add hand strength progression features

3. **Consider hybrid approach**
   - Use decision trees for explanation
   - Use neural networks for action selection
   - Combine both for best of both worlds

---

## Performance Expectations

### Realistic Goals
- **Win rate**: 60-70% (vs DeepCFR's 86%)
- **Avg profit**: $4-6/game (vs DeepCFR's $7.68)
- **Interpretable agent will always be weaker** than DeepCFR due to:
  - Simpler model (decision trees vs neural networks)
  - Limited feature space
  - Binary decision structure

### Trade-offs
- **Interpretability** comes at the cost of **performance**
- **Decision trees** are easier to understand but less expressive than neural networks
- **Feature count** is limited (35 vs 500+ in DeepCFR)

---

## Conclusion

The interpretable agent is **significantly underperforming** compared to DeepCFR:
- **512.8% worse** in average profit per game
- **30 percentage points lower** win rate
- **Imbalanced action distribution** (too many folds, too few calls)

**Primary issues**:
1. Trees trained without betting history features
2. Betting history tracking not working properly
3. Decision trees inherently less expressive than neural networks

**Next steps**:
1. Retrain trees with betting history features
2. Fix betting history tracking
3. Accept that interpretable agent will be weaker but more explainable

