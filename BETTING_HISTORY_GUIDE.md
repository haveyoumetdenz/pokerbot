# Betting History & Strategic Agent Guide

## 📊 **Betting History Implementation**

### **What Was Added:**
- **Cumulative betting history** tracking across all games
- **Per-opponent statistics**: VPIP, PFR, aggression factor, action frequencies
- **Street-level statistics**: Raise/call/fold frequencies per street
- **12 new features** for decision trees:
  - `street_raise_frequency`, `street_call_frequency`, `street_fold_frequency`
  - `street_aggression_factor`
  - `avg_opponent_raise_frequency`, `avg_opponent_call_frequency`, `avg_opponent_fold_frequency`
  - `avg_opponent_aggression`, `avg_opponent_vpip`, `avg_opponent_pfr`
  - `games_played`

### **How It Works:**
1. **Automatic tracking**: Actions are recorded automatically during gameplay
2. **Cumulative**: Statistics accumulate across all games
3. **Per-opponent**: Each opponent's patterns are tracked separately
4. **Features**: Decision trees can use betting history to make informed decisions

---

## 🔄 **Retraining the Interpretable Agent**

### **Why Retrain?**
The current decision trees were trained **without** betting history features. To use these new features, you need to retrain.

### **How to Retrain:**

```bash
# Retrain with betting history features included
python scripts/train_interpretable_complete.py \
  --iterations 3000 \
  --traversals 400 \
  --tree-depth 15 \
  --output-dir interpretable_output/models/
```

**What this does:**
1. Runs CFR training with data collection (collects decisions with betting history)
2. Trains decision trees with all features (including the new betting history features)
3. Saves new trees that can use betting history for decisions

**Note:** The betting history features will start with default values (0.33, 0.33, etc.) and improve as you play more games and accumulate history.

---

## 🎯 **Strategic Agent (Hand Range-Based)**

### **What It Does:**
The `StrategicAgent` follows calling ranges based on:
- **Pot odds** (how favorable the pot odds are)
- **Tightness level** (very tight, tight, average, loose, very loose, any two)
- **Hand strength** (checks if your hand is in the calling range)

### **How to Use StrategicAgent:**

**Option 1: In your code**
```python
from src.agents.strategic_agent import StrategicAgent

# Create strategic opponents
strategic_opponents = [
    StrategicAgent(player_id=1, tightness='average'),
    StrategicAgent(player_id=2, tightness='tight'),
    StrategicAgent(player_id=3, tightness='loose'),
    StrategicAgent(player_id=4, tightness='very_tight'),
    StrategicAgent(player_id=5, tightness='average')
]
```

**Option 2: Update demo scripts**
Modify `demo_interpretable.py` or `compare_agents.py` to use StrategicAgent instead of RandomAgent.

### **Tightness Levels:**
- `'very_tight'` (3%): Only calls with premium hands (AA-QQ, AK)
- `'tight'` (5%): Calls with strong hands (AA-JJ, AK-AQ)
- `'average'` (10%): Balanced calling strategy
- `'loose'` (25%): Calls with many hands
- `'very_loose'` (50%): Calls with most hands
- `'any_two'` (100%): Calls with almost anything

### **Pot Odds Categories:**
- `'6_to_5'`: Best pot odds (pot ≥ 10x the call) → tightest calling range
- `'3_to_2'`: Good pot odds (pot ≥ 4x the call) → tighter calling range
- `'2_to_1'`: Moderate pot odds (pot ≥ 1.8x the call) → looser calling range
- `'worse'`: Poor pot odds → fold (unless very strong hand)

---

## 🚀 **Quick Start**

### **1. Retrain Interpretable Agent with Betting History:**
```bash
python scripts/train_interpretable_complete.py \
  --iterations 3000 \
  --traversals 400 \
  --tree-depth 15 \
  --output-dir interpretable_output/models/
```

### **2. Test with Strategic Agents:**
Update your demo scripts to use `StrategicAgent` instead of `RandomAgent` for more realistic opponents.

### **3. Play Games:**
As you play games, betting history accumulates automatically. The interpretable agent's decisions will improve as it learns opponent patterns.

---

## 📝 **Notes**

- **Betting history is cumulative**: It persists across games, so the agent learns opponent patterns over time
- **Default values**: Initially, history features use default values (0.33, 0.33, etc.) until enough games are played
- **Per-opponent tracking**: Each opponent's statistics are tracked separately, allowing the agent to adapt to different playing styles
- **Strategic agent**: Uses hand ranges based on professional poker strategy tables

