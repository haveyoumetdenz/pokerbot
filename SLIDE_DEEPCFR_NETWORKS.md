# DeepCFR Networks: Slide Content

---

## Slide 1: Two Networks Overview

### **DeepCFR Uses Two Neural Networks**

```
┌─────────────────────┐         ┌─────────────────────┐
│  Advantage Network  │         │  Strategy Network   │
│  (Regret Learning)  │         │  (Final Policy)     │
└─────────────────────┘         └─────────────────────┘
         │                               │
         ▼                               ▼
    "What should I              "What will I
     have done?"                 do?"
```

**Key Point**: They work together but serve different purposes!

---

## Slide 2: Advantage Network

### **What is it?**
- Estimates **counterfactual regrets** for each action
- Regret = "How much better would I have done with a different action?"

### **How it works:**
1. **During Training:**
   - Predicts advantages: `[advantage_fold, advantage_call, advantage_raise]`
   - Converts to strategy using **Regret Matching**
   - Calculates actual regrets from game outcomes
   - Trains to predict these regrets

2. **Regret Matching Formula:**
   ```
   positive_regrets = max(advantages, 0)
   strategy = positive_regrets / sum(positive_regrets)
   ```

### **Training Details:**
- **Loss**: Smooth L1 Loss (Huber)
- **Memory**: Prioritized Experience Replay
- **Learning Rate**: **1e-6** (very small!)
- **Optimizer**: **Adam** (weight decay: 1e-5)

---

## Slide 3: Strategy Network

### **What is it?**
- Learns the **final playing strategy**
- Outputs action probabilities: `[P(fold), P(call), P(raise)]`

### **How it works:**
1. **During Training:**
   - Collects strategies from CFR traversal
   - Weights by iteration number (Linear CFR)
   - Trains to match these strategies

2. **During Play:**
   - Outputs action probabilities
   - Samples action from distribution
   - Uses predicted bet size for raises

### **Training Details:**
- **Loss**: Weighted Cross-Entropy
- **Memory**: Standard replay buffer
- **Learning Rate**: **5e-5** (0.00005)
- **Optimizer**: **Adam** (weight decay: 1e-5)

---

## Slide 4: Optimizer - Adam

### **Adam (Adaptive Moment Estimation)**

**Used by both networks:**
- **Adaptive learning rates** per parameter
- **Momentum** for faster convergence
- **Bias correction** for better estimates

**Configuration:**
```
Advantage Network:  lr = 1e-6,  weight_decay = 1e-5
Strategy Network:   lr = 5e-5,  weight_decay = 1e-5
```

**Why different learning rates?**
- Regret learning is **unstable** → needs very small LR
- Strategy learning is **more stable** → can use larger LR

**Additional Stabilization:**
- Gradient clipping (max norm = 0.5)
- L2 regularization (weight decay)

---

## Slide 5: How They Work Together

### **Training Phase:**
```
State → Advantage Network → Regret Matching → Strategy
                                    ↓
                            Collect & Weight by Iteration
                                    ↓
                            Train Strategy Network
```

### **Playing Phase:**
```
State → Strategy Network → Sample Action → Play!
```

### **Key Insight:**
- **Advantage network** guides learning (what's good?)
- **Strategy network** is what we actually use (how to play)

---

## Slide 6: Comparison Table

| Feature | Advantage Network | Strategy Network |
|---------|------------------|------------------|
| **Role** | Learn regrets | Learn strategy |
| **Output** | Advantage values | Probabilities |
| **Used When** | Training only | Training + Play |
| **Learning Rate** | 1e-6 | 5e-5 |
| **Memory** | Prioritized | Standard |
| **Loss** | Smooth L1 | Cross-Entropy |

---

## Slide 7: Why Two Networks?

### **1. Separation of Concerns**
- Different objectives → different networks
- Easier to optimize each separately

### **2. Stability**
- Regret learning can be noisy
- Isolated network prevents instability

### **3. Efficiency**
- During play: only strategy network needed
- Faster inference

### **4. Theory Alignment**
- Matches traditional CFR structure
- Regrets → Strategy via regret matching

---

## Slide 8: Key Takeaways

### **Remember:**
1. **Advantage Network** = "What should I have done?" (regret)
2. **Strategy Network** = "What will I do?" (policy)
3. Both use **Adam optimizer** with different learning rates
4. They work together: advantages → strategy → action
5. This is the **core of Deep CFR** algorithm

### **The Flow:**
```
Training:  State → Advantages → Regrets → Strategy → Train Both Networks
Playing:   State → Strategy → Action
```


