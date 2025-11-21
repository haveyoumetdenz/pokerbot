# Progressive Training Pipeline for Interpretable Poker AI

## Overview

This progressive training pipeline trains the interpretable agent through multiple phases, exposing it to increasingly sophisticated opponents. This approach produces more robust and generalizable decision trees.

## Training Pipeline

### Phase 1: Random Opponents
- **Purpose**: Learn fundamental poker concepts
- **Opponents**: Random agents
- **Goal**: Develop basic strategy

### Phase 2: Strategic Opponents
- **Purpose**: Learn to adapt to rule-based opponents
- **Opponents**: Strategic agents with mixed tightness levels
- **Goal**: Develop adaptive strategies

### Phase 3: Mixed Opponents
- **Purpose**: Learn robust strategies
- **Opponents**: Mix of random and strategic agents
- **Goal**: Develop generalizable strategies

### Phase 4: Data Collection
- **Purpose**: Collect diverse training data
- **Opponents**: All types (random, strategic, mixed)
- **Goal**: Create comprehensive dataset

### Phase 5: Decision Tree Training
- **Purpose**: Train interpretable decision trees
- **Input**: Collected data from Phase 4
- **Goal**: Create interpretable agent

## Usage

### Full Pipeline (Recommended)

```bash
python scripts/train_progressive.py \
    --phase1-iterations 1000 \
    --phase2-iterations 1000 \
    --phase3-iterations 1000 \
    --traversals 200 \
    --data-collection-games 500 \
    --output-dir progressive_training
```

### Quick Training (Faster)

```bash
python scripts/train_progressive.py \
    --phase1-iterations 500 \
    --phase2-iterations 500 \
    --phase3-iterations 500 \
    --traversals 100 \
    --data-collection-games 200 \
    --output-dir progressive_training_quick
```

### Skip Specific Phases

```bash
# Skip Phase 1 (if already trained)
python scripts/train_progressive.py \
    --skip-phase 1 \
    --phase2-iterations 1000 \
    --phase3-iterations 1000
```

### Individual Phase Training

You can also train individual phases:

```bash
# Phase 1: Random
python -m src.training.train_interpretable \
    --iterations 1000 \
    --traversals 200 \
    --opponent-type random \
    --data-dir data/interpretable

# Phase 2: Strategic (continue from Phase 1)
python -m src.training.train_interpretable \
    --iterations 1000 \
    --traversals 200 \
    --opponent-type strategic \
    --opponent-tightness mixed \
    --checkpoint models/interpretable_cfr_checkpoint_iter_1000.pt \
    --data-dir data/interpretable

# Phase 3: Mixed (continue from Phase 2)
python -m src.training.train_interpretable \
    --iterations 1000 \
    --traversals 200 \
    --opponent-type mixed \
    --checkpoint models/interpretable_cfr_checkpoint_iter_2000.pt \
    --data-dir data/interpretable
```

## Arguments

### Progressive Training Script

| Argument | Default | Description |
|----------|---------|-------------|
| `--phase1-iterations` | 1000 | Iterations for Phase 1 (random) |
| `--phase2-iterations` | 1000 | Iterations for Phase 2 (strategic) |
| `--phase3-iterations` | 1000 | Iterations for Phase 3 (mixed) |
| `--traversals` | 200 | Traversals per iteration |
| `--data-collection-games` | 500 | Games per opponent type for Phase 4 |
| `--skip-phase` | None | Skip specific phases (1, 2, 3, or 4) |
| `--output-dir` | `progressive_training` | Output directory |
| `--tree-depth` | 12 | Maximum tree depth |
| `--verbose` | False | Enable verbose output |

### Individual Training Script

| Argument | Default | Description |
|----------|---------|-------------|
| `--iterations` | 1000 | Number of CFR iterations |
| `--traversals` | 200 | Traversals per iteration |
| `--opponent-type` | `random` | Type: `random`, `strategic`, or `mixed` |
| `--opponent-tightness` | `average` | For strategic: `very_tight`, `tight`, `average`, `loose`, `very_loose`, `mixed` |
| `--checkpoint` | None | Path to checkpoint to continue from |
| `--data-dir` | `data/interpretable` | Directory to save collected data |
| `--save-dir` | `models` | Directory to save models |
| `--log-dir` | `logs/interpretable_cfr` | Directory for logs |
| `--verbose` | False | Enable verbose output |

## Output Structure

```
progressive_training/
├── models/              # Trained DeepCFR models
│   ├── interpretable_cfr_agent.pt
│   ├── interpretable_cfr_checkpoint_iter_1000.pt
│   ├── interpretable_cfr_checkpoint_iter_2000.pt
│   └── interpretable_cfr_checkpoint_iter_3000.pt
├── data/                # Collected training data (Parquet format)
│   ├── preflop_decisions.parquet
│   ├── flop_decisions.parquet
│   ├── turn_decisions.parquet
│   ├── river_decisions.parquet
│   └── collection_stats.json
├── trees/               # Trained decision trees
│   ├── preflop_tree.pkl
│   ├── flop_tree.pkl
│   ├── turn_tree.pkl
│   ├── river_tree.pkl
│   └── training_stats.json
└── logs/                # Training logs
    ├── phase1_random/
    ├── phase2_strategic/
    └── phase3_mixed/
```

## Benefits

1. **Better Generalization**: Trees see diverse opponents during training
2. **More Balanced Actions**: Not just aggressive vs random
3. **Better Performance**: Trees learn robust strategies
4. **More Interpretable**: Still explainable with better quality

## Time Estimates

| Phase | Iterations | Time (approx) |
|-------|------------|---------------|
| Phase 1 | 1000 | ~18-20 hours |
| Phase 2 | 1000 | ~18-20 hours |
| Phase 3 | 1000 | ~18-20 hours |
| Phase 4 | 500 games × 3 types | ~2-3 hours |
| Phase 5 | Tree training | ~10-15 minutes |
| **Total** | | **~60-65 hours** |

For quick training (500 iterations each):
- **Total**: ~30-35 hours

## Next Steps

After training:

1. **Evaluate the agent**:
   ```bash
   python compare_agents.py \
       --num-games 500 \
       --opponent-type strategic \
       --interpretable-dir progressive_training/trees
   ```

2. **Visualize decision trees**:
   ```bash
   python scripts/visualize_interpretable_trees.py \
       --tree-dir progressive_training/trees
   ```

3. **Play against the agent**:
   ```bash
   python scripts/play.py \
       --tree-dir progressive_training/trees
   ```


