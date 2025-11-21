# DeepCFR Networks: Advantage & Strategy Networks

## Slide Content: Understanding the Two Networks

---

## 🎯 **Overview: Two Networks, Two Roles**

The DeepCFR agent uses **two separate neural networks** that work together:

1. **Advantage Network** → Learns what actions are "good" (regret estimation)
2. **Strategy Network** → Learns how to play (final strategy)

---

## 📊 **1. Advantage Network (Regret Learning)**

### **What it means conceptually:**
- **Regret** = "How much better would I have done if I chose a different action?"
- The advantage network estimates **counterfactual regrets** for each action
- It answers: *"What's the advantage of taking action A vs. the average?"*

### **How it works generally:**
- In traditional CFR: Regrets are stored in a lookup table
- In Deep CFR: A neural network **approximates** regrets for any state
- Uses **Regret Matching**: Actions with positive regret get higher probability

### **How it works in this implementation:**

**During Training (CFR Traversal):**
```
1. Network predicts advantages for each action: [advantage_fold, advantage_call, advantage_raise]
2. Convert to strategy using Regret Matching:
   - Only positive advantages count
   - Strategy = positive_advantages / sum(positive_advantages)
3. Calculate actual regrets: regret = action_value - expected_value
4. Train network to predict these regrets (target = weighted_regret)
```

**Training Details:**
- **Loss Function**: Smooth L1 Loss (Huber loss) between predicted and actual regrets
- **Memory**: Prioritized Experience Replay (high regret states sampled more often)
- **Learning Rate**: **1e-6** (very small for stability)
- **Optimizer**: **Adam** with weight decay 1e-5

**Key Code:**
```python
# During CFR traversal
advantages, bet_size = self.advantage_net(state)
advantages_masked = max(advantages[a], 0)  # Only positive regrets
strategy = advantages_masked / sum(advantages_masked)  # Regret matching

# Training
predicted_regret = advantage_net(state)[action]
actual_regret = action_value - expected_value
loss = smooth_l1_loss(predicted_regret, actual_regret)
```

---

## 🎮 **2. Strategy Network (Final Policy)**

### **What it means conceptually:**
- The **final strategy** the agent uses to play
- Represents the learned Nash equilibrium approximation
- Answers: *"What's the probability I should take each action?"*

### **How it works generally:**
- In traditional CFR: Average strategy over all iterations
- In Deep CFR: Neural network learns to output action probabilities directly
- Uses **Linear CFR weighting**: Recent iterations weighted more heavily

### **How it works in this implementation:**

**During Training:**
```
1. Collect strategies from CFR traversal (weighted by iteration number)
2. Store: (state, strategy_distribution, iteration_number)
3. Train network to predict strategy distribution
4. Network outputs: [prob_fold, prob_call, prob_raise]
```

**During Play:**
```
1. Network outputs action probabilities
2. Sample action from this distribution
3. Use predicted bet size for raise actions
```

**Training Details:**
- **Loss Function**: Weighted Cross-Entropy (KL divergence from target strategy)
- **Memory**: Standard replay buffer (deque)
- **Learning Rate**: **5e-5** (0.00005)
- **Optimizer**: **Adam** with weight decay 1e-5
- **Weighting**: Samples weighted by iteration (Linear CFR)

**Key Code:**
```python
# During play
action_logits, bet_size = self.strategy_net(state)
probs = softmax(action_logits)  # [prob_fold, prob_call, prob_raise]
action = sample(probs)  # Choose action probabilistically

# Training
predicted_strategy = softmax(strategy_net(state))
target_strategy = collected_strategy  # From CFR traversal
loss = -sum(weight * target * log(predicted))  # Weighted cross-entropy
```

---

## ⚙️ **Optimizer Details**

### **Adam Optimizer**
Both networks use **Adam (Adaptive Moment Estimation)**:

**Advantage Network:**
- Learning Rate: **1e-6** (0.000001)
- Weight Decay: **1e-5** (L2 regularization)
- Why so small? Regret values can be unstable, needs careful learning

**Strategy Network:**
- Learning Rate: **5e-5** (0.00005) 
- Weight Decay: **1e-5** (L2 regularization)
- Why larger? Strategy is more stable, can learn faster

**Additional Stabilization:**
- **Gradient Clipping**: Max norm = 0.5 (prevents exploding gradients)
- **Prioritized Replay**: Advantage network samples high-regret states more often
- **Normalization**: Regrets normalized before training

---

## 🔄 **How They Work Together**

```
┌─────────────────────────────────────────────────────────┐
│                    Training Phase                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. CFR Traversal:                                       │
│     ┌──────────────┐                                     │
│     │ State        │                                     │
│     └──────┬───────┘                                     │
│            │                                             │
│            ▼                                             │
│     ┌──────────────┐      ┌──────────────┐             │
│     │ Advantage    │─────▶│ Strategy     │             │
│     │ Network      │      │ (Regret      │             │
│     │              │      │  Matching)   │             │
│     └──────┬───────┘      └──────┬───────┘             │
│            │                     │                       │
│            ▼                     ▼                       │
│     Calculate Regrets    Collect Strategy               │
│            │                     │                       │
│            ▼                     ▼                       │
│     Train Advantage Net  Train Strategy Net             │
│                                                          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    Playing Phase                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│     ┌──────────────┐                                     │
│     │ State        │                                     │
│     └──────┬───────┘                                     │
│            │                                             │
│            ▼                                             │
│     ┌──────────────┐                                    │
│     │ Strategy      │                                    │
│     │ Network       │                                    │
│     │ (Final        │                                    │
│     │  Policy)      │                                    │
│     └──────┬───────┘                                    │
│            │                                            │
│            ▼                                            │
│     Sample Action                                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 **Key Differences Summary**

| Aspect | Advantage Network | Strategy Network |
|--------|------------------|-------------------|
| **Purpose** | Learn regrets (what's good) | Learn strategy (how to play) |
| **Output** | Advantage values (can be negative) | Action probabilities (sum to 1) |
| **Used During** | Training (CFR traversal) | Both training & playing |
| **Learning Rate** | 1e-6 (very small) | 5e-5 (small) |
| **Memory Type** | Prioritized Replay | Standard Replay |
| **Loss Function** | Smooth L1 (regret prediction) | Cross-Entropy (strategy matching) |
| **Weighting** | By regret magnitude | By iteration number |

---

## 💡 **Why Two Networks?**

1. **Separation of Concerns**: 
   - Advantage network focuses on learning "what's good"
   - Strategy network focuses on learning "how to play"

2. **Stability**: 
   - Regret learning can be noisy → separate network prevents instability
   - Strategy network learns from accumulated, weighted strategies

3. **Efficiency**:
   - During play, only strategy network needed (faster inference)
   - Advantage network only used during training

4. **CFR Theory**:
   - Matches traditional CFR: regrets → strategy via regret matching
   - Deep CFR approximates both with neural networks

---

## 🎓 **Takeaway Points**

1. **Advantage Network** = "What should I have done?" (regret learning)
2. **Strategy Network** = "What will I do?" (final policy)
3. Both use **Adam optimizer** with different learning rates
4. They work together: advantages → strategy during training, strategy → action during play
5. This dual-network approach is the core of Deep CFR algorithm


