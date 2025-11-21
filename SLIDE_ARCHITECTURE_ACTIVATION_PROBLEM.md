# Deep CFR Architecture, Activation, and Problem Type

---

## Slide 1: Deep CFR Network Architecture

### **Architecture Overview**

Both **Advantage Network** and **Strategy Network** use the same architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT LAYER                          │
│              500 dimensions (poker state)               │
│  [Cards, Pot, Positions, Player States, Legal Actions] │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  HIDDEN LAYERS                          │
│                                                          │
│  Layer 1: 256 neurons + ReLU                            │
│  Layer 2: 256 neurons + ReLU                            │
│  Layer 3: 256 neurons + ReLU                            │
│                                                          │
│  (Shared feature extraction)                             │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌──────────────────┐   ┌──────────────────────┐
│  ACTION HEAD     │   │  BET SIZING HEAD     │
│  256 → 3         │   │  256 → 128 (Tanh)    │
│  (No activation) │   │  128 → 1 (Sigmoid)   │
│                  │   │  Scaled: 0.1-3.0x    │
│  [Fold, Call,    │   │  pot multiplier      │
│   Raise logits]  │   │                      │
└──────────────────┘   └──────────────────────┘
```

### **Architecture Specifications:**

| Component | Details |
|-----------|---------|
| **Input Layer** | 500 dimensions (poker state encoding) |
| **Hidden Layer 1** | 256 neurons + **ReLU** activation |
| **Hidden Layer 2** | 256 neurons + **ReLU** activation |
| **Hidden Layer 3** | 256 neurons + **ReLU** activation |
| **Output Branch 1** | 3 neurons (action logits: fold, call, raise) |
| **Output Branch 2** | 1 neuron (bet size multiplier: 0.1-3.0x pot) |

**Total Parameters**: ~200K per network (advantage + strategy = ~400K total)

---

## Slide 2: ReLU Activation Function

### **What is ReLU?**

**ReLU** = **Rectified Linear Unit**

**Mathematical Definition:**
```
ReLU(x) = max(0, x) = {
    x   if x > 0
    0   if x ≤ 0
}
```

**Visual Representation:**
```
     │
     │    ╱
     │   ╱
─────┼───╱─────
     │ ╱
     │╱
```

### **How ReLU Works Generally:**

1. **Non-linearity**: Introduces non-linearity to neural networks
   - Without activation: network is just linear transformations
   - With ReLU: network can learn complex patterns

2. **Sparsity**: Sets negative values to zero
   - Creates sparse representations
   - Only ~50% of neurons active at a time
   - More efficient computation

3. **Gradient Flow**: 
   - Gradient = 1 for positive inputs (no vanishing gradient)
   - Gradient = 0 for negative inputs (dead neurons possible)

4. **Computational Efficiency**:
   - Very fast to compute (just max operation)
   - No expensive exponentials like sigmoid/tanh

### **Why ReLU is Popular:**
- ✅ Solves vanishing gradient problem (better than sigmoid/tanh)
- ✅ Fast computation
- ✅ Sparse activations (efficient)
- ✅ Works well in deep networks

---

## Slide 3: How ReLU is Used in Deep CFR

### **In Our Architecture:**

**Hidden Layers (3 layers):**
```python
Layer 1: Linear(500 → 256) → ReLU
Layer 2: Linear(256 → 256) → ReLU  
Layer 3: Linear(256 → 256) → ReLU
```

**Why ReLU for Hidden Layers?**

1. **Feature Extraction**:
   - ReLU helps extract meaningful poker features
   - Hand strength, pot odds, position → encoded in activations
   - Negative values (bad features) are suppressed

2. **Deep Learning Benefits**:
   - 3 hidden layers need good gradient flow
   - ReLU prevents vanishing gradients
   - Allows network to learn hierarchical features:
     - Layer 1: Basic features (card values, positions)
     - Layer 2: Combined features (hand strength + pot size)
     - Layer 3: Complex features (strategic patterns)

3. **Poker-Specific Advantages**:
   - Poker has many "zero" states (folded players, no action)
   - ReLU naturally handles sparse inputs
   - Efficient for large state space (500 dimensions)

### **Other Activations in Our Network:**

**Bet Sizing Head:**
- **Tanh**: Bounds intermediate values (-1 to 1)
- **Sigmoid**: Final output (0 to 1), then scaled to 0.1-3.0x pot

**Action Head:**
- **No activation**: Raw logits (used with softmax later)

---

## Slide 4: Problem Type

### **What Problem Are We Solving?**

**Reinforcement Learning Problem:**
- **Domain**: Texas No-Limit Hold'em Poker (6 players)
- **Algorithm**: Deep Counterfactual Regret Minimization (Deep CFR)
- **Goal**: Learn Nash equilibrium strategy

### **Problem Characteristics:**

1. **Imperfect Information Game**:
   - Players don't see opponents' cards
   - Must reason about hidden information
   - Much harder than perfect information games (chess, go)

2. **Large State Space**:
   - 500-dimensional state encoding
   - Millions of possible game states
   - Cannot use tabular methods (too large)

3. **Sequential Decision Making**:
   - Multiple betting rounds (preflop, flop, turn, river)
   - Decisions affect future states
   - Need to plan ahead

4. **Multi-Agent Environment**:
   - 6 players competing
   - Opponents have different strategies
   - Must adapt to various playing styles

### **Why Deep CFR?**

**Traditional CFR Limitations:**
- Requires storing regrets for every state
- Impossible for large state spaces
- Memory and computation explode

**Deep CFR Solution:**
- Neural networks **approximate** regrets
- Generalize to unseen states
- Handle continuous bet sizing
- Scalable to complex poker games

### **Problem Formulation:**

```
Given: Poker game state s
Find: Optimal action probabilities π(s)

Method: Minimize counterfactual regret
        → Learn Nash equilibrium strategy
        → Play optimally against any opponent
```

---

## Slide 5: Architecture Summary

### **Complete Network Structure**

```
INPUT (500D)
    │
    ├─→ Linear(500 → 256) → ReLU
    │
    ├─→ Linear(256 → 256) → ReLU
    │
    ├─→ Linear(256 → 256) → ReLU
    │
    ├─→ ACTION HEAD: Linear(256 → 3) → [logits]
    │
    └─→ BET SIZING HEAD:
        ├─→ Linear(256 → 128) → Tanh
        └─→ Linear(128 → 1) → Sigmoid → Scale(0.1-3.0x)
```

### **Key Design Choices:**

1. **3 Hidden Layers**: 
   - Deep enough to learn complex patterns
   - Shallow enough to train efficiently

2. **256 Neurons per Layer**:
   - Balance between capacity and efficiency
   - Sufficient for poker state representation

3. **ReLU Activation**:
   - Standard for deep learning
   - Prevents vanishing gradients
   - Efficient computation

4. **Dual Output Heads**:
   - Separate action type and bet sizing
   - Allows independent learning
   - Matches poker's discrete + continuous nature

---

## Slide 6: Why This Architecture Works

### **For Poker Specifically:**

1. **Input Encoding (500D)**:
   - Captures all relevant game information
   - Cards, pot, positions, player states
   - Legal actions, previous actions

2. **Hidden Layers (256 neurons × 3)**:
   - Learn poker concepts:
     - Hand strength evaluation
     - Pot odds calculation
     - Positional awareness
     - Opponent modeling patterns

3. **ReLU Activation**:
   - Handles sparse poker states (folded players)
   - Efficient for large input space
   - Good gradient flow for deep network

4. **Output Design**:
   - **Action logits**: Discrete action choice
   - **Bet sizing**: Continuous value (0.1-3.0x pot)
   - Matches poker's action space perfectly

### **Architecture Advantages:**

✅ **Scalable**: Works for any poker variant
✅ **Efficient**: Fast inference during play
✅ **Expressive**: Can learn complex strategies
✅ **Stable**: ReLU prevents common training issues

---

## Slide 7: Quick Reference

### **Architecture at a Glance**

| Component | Specification |
|-----------|--------------|
| **Input Size** | 500 dimensions |
| **Hidden Layers** | 3 layers |
| **Neurons per Layer** | 256 |
| **Activation (Hidden)** | ReLU |
| **Activation (Bet Sizing)** | Tanh → Sigmoid |
| **Action Output** | 3 logits (fold, call, raise) |
| **Bet Size Output** | 1 value (0.1-3.0x pot) |
| **Total Networks** | 2 (advantage + strategy) |

### **ReLU Formula:**
```
ReLU(x) = max(0, x)
```

### **Problem Type:**
- **Category**: Reinforcement Learning
- **Game**: Imperfect Information, Multi-Agent
- **Algorithm**: Deep CFR (Neural Network + CFR)
- **Objective**: Nash Equilibrium Strategy


