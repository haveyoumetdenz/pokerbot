# Interpretable Deep CFR Poker AI

This project extends the Deep CFR poker AI with interpretable decision trees, following the approach described in "World-class interpretable poker" (Bertsimas & Paskov, 2022). The system provides full transparency into poker decision-making while maintaining competitive performance.

## 🎯 Overview

The interpretable poker AI replaces the black-box neural networks with transparent decision trees that can be easily understood and analyzed. This makes the system suitable for:

- **Research**: Understanding poker strategy and decision-making
- **Teaching**: Learning poker concepts through AI explanations
- **Analysis**: Studying betting patterns and strategic principles
- **Debugging**: Identifying and fixing decision-making issues

## 🏗️ Architecture

### Core Components

1. **Feature Engineering** (`src/interpretable/feature_extractor.py`)
   - Extracts 22 interpretable features from poker states
   - Replaces 500-dimensional neural network input
   - Features include hand equity, pot odds, position, betting history

2. **Data Collection** (`src/interpretable/data_collector.py`)
   - Records CFR decisions with interpretable features
   - Aggregates data by betting round (preflop, flop, turn, river)
   - Exports training data as CSV files

3. **Decision Tree Training** (`src/interpretable/tree_trainer.py`)
   - Trains separate trees for each betting round
   - Uses grid search for hyperparameter optimization
   - Balances accuracy with interpretability

4. **Interpretable Agent** (`src/interpretable/interpretable_agent.py`)
   - Uses decision trees for action selection
   - Provides decision explanations
   - Maintains decision history for analysis

5. **Visualization Tools** (`src/interpretable/visualizer.py`)
   - Exports trees as images, text, and markdown
   - Generates strategy charts and opening ranges
   - Creates human-readable decision rules

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
pip install scikit-learn graphviz matplotlib seaborn pandas
```

### 2. Train Interpretable Agent

```bash
# Step 1: Collect training data with CFR
python -m src.training.train_interpretable --iterations 1000 --traversals 200

# Step 2: Train decision trees
python -m src.interpretable.tree_trainer --data-dir data/interpretable --output-dir models/interpretable

# Step 3: Visualize trees
python scripts/visualize_interpretable_trees.py --tree-dir models/interpretable
```

### 3. Evaluate Performance

```bash
# Evaluate against random opponents
python scripts/evaluate_interpretable.py --tree-dir models/interpretable --num-games 1000

# Compare with neural network
python scripts/evaluate_interpretable.py --tree-dir models/interpretable --neural-model models/deep_cfr_agent.pt
```

### 4. Interactive Analysis

```bash
# Launch Jupyter notebook for interactive exploration
jupyter notebook notebooks/interpretable_analysis.ipynb
```

## 📊 Features

### Interpretable Features (22 total)

| Feature | Description | Example |
|---------|-------------|---------|
| `hand_equity` | Probability of winning (0-1) | 0.75 |
| `equity_percentile` | Hand strength percentile (0-100) | 85 |
| `pot_size_bb` | Pot size in big blinds | 12.5 |
| `pot_odds` | Pot odds for calling (0-1) | 0.33 |
| `position_numeric` | Position at table (0-3) | 2 (middle) |
| `stack_size_bb` | Stack size in big blinds | 50.0 |
| `street_numeric` | Betting round (0-3) | 1 (flop) |
| `aggression_factor` | Betting aggression measure | 0.6 |

### Decision Tree Outputs

Each tree predicts one of three actions:
- **Fold**: Give up the hand
- **Call**: Match the current bet
- **Raise**: Increase the bet amount

### Explanation Format

```
Decision: RAISE - Raise for value or as a bluff
Hand equity: 75.0%
Pot odds: 33.3%
Position: late
Pot size: 12.5 BB
Decision path:
  - hand_equity > 0.600
  - pot_odds <= 0.400
  - position_numeric > 2
```

## 🔧 Usage Examples

### Basic Agent Usage

```python
from src.interpretable.interpretable_agent import InterpretablePokerAgent
import pokers as pkrs

# Create agent
agent = InterpretablePokerAgent(player_id=0, tree_dir='models/interpretable')

# Get decision
state = pkrs.State.from_seed(n_players=6, button=0, sb=1, bb=2, stake=200.0)
action = agent.choose_action(state)

# Get explanation
explanation = agent.explain_decision(state)
print(explanation['explanation'])
```

### Training Custom Trees

```python
from src.interpretable.tree_trainer import InterpretableTreeTrainer

# Train trees
trainer = InterpretableTreeTrainer(max_depth=10)
trees = trainer.train_all_trees('data/interpretable')
trainer.save_trees('models/interpretable')

# Evaluate performance
results = trainer.evaluate_trees('data/interpretable')
```

### Visualization

```python
from src.interpretable.visualizer import visualize_tree, export_tree_as_markdown

# Load tree
import joblib
tree = joblib.load('models/interpretable/preflop_tree.pkl')

# Create visualizations
visualize_tree(tree, feature_names, 'preflop_tree', 'preflop')
export_tree_as_markdown(tree, feature_names, 'preflop_rules.md', 'preflop')
```

## 📈 Performance

### Typical Results

- **vs Random Opponents**: 15-25 BB/100 profit
- **Decision Accuracy**: 85-95% vs CFR ground truth
- **Tree Complexity**: 6-12 depth, 50-200 leaves per tree
- **Decision Time**: <1ms per decision

### Interpretability Benefits

- **Full Transparency**: Every decision can be explained
- **Human-Readable Rules**: Easy to understand and modify
- **Strategy Analysis**: Identify key decision factors
- **Teaching Tool**: Learn poker through AI explanations

## 🎓 Educational Use

### Learning Poker Concepts

The interpretable AI helps learn poker by:

1. **Showing Decision Factors**: See which features matter most
2. **Explaining Reasoning**: Understand why each decision was made
3. **Strategy Patterns**: Identify common betting patterns
4. **Position Play**: Learn how position affects decisions

### Example Learning Scenarios

```python
# Scenario 1: Strong hand in late position
features = {
    'hand_equity': 0.85,
    'position': 'late',
    'pot_size_bb': 8.0,
    'street': 'flop'
}
# Expected: RAISE (value betting)

# Scenario 2: Weak hand in early position
features = {
    'hand_equity': 0.25,
    'position': 'early',
    'pot_size_bb': 12.0,
    'street': 'turn'
}
# Expected: FOLD (weak hand, poor position)
```

## 🔍 Analysis Tools

### Jupyter Notebook

The `notebooks/interpretable_analysis.ipynb` provides:

- Interactive tree exploration
- Feature importance analysis
- Decision path visualization
- Performance comparison
- Strategy chart generation

### Command Line Tools

```bash
# Visualize all trees
python scripts/visualize_interpretable_trees.py --tree-dir models/interpretable

# Evaluate performance
python scripts/evaluate_interpretable.py --tree-dir models/interpretable --num-games 1000

# Train new trees
python -m src.interpretable.tree_trainer --data-dir data/interpretable --max-depth 12
```

## 📁 File Structure

```
src/interpretable/
├── __init__.py                 # Package initialization
├── feature_extractor.py        # Feature extraction
├── data_collector.py          # Data collection
├── tree_trainer.py            # Tree training
├── interpretable_agent.py      # Interpretable agent
└── visualizer.py              # Visualization tools

scripts/
├── visualize_interpretable_trees.py  # Tree visualization
└── evaluate_interpretable.py        # Performance evaluation

notebooks/
└── interpretable_analysis.ipynb     # Interactive analysis

data/interpretable/
├── preflop_decisions.csv       # Preflop training data
├── flop_decisions.csv         # Flop training data
├── turn_decisions.csv         # Turn training data
└── river_decisions.csv        # River training data

models/interpretable/
├── preflop_tree.pkl           # Preflop decision tree
├── flop_tree.pkl             # Flop decision tree
├── turn_tree.pkl             # Turn decision tree
├── river_tree.pkl            # River decision tree
└── training_stats.json       # Training statistics

visualizations/trees/
├── preflop_tree.png          # Tree visualization
├── preflop_rules.md          # Human-readable rules
├── flop_tree.png             # Tree visualization
├── flop_rules.md             # Human-readable rules
└── strategy_chart.md         # Comprehensive strategy guide
```

## 🧪 Research Applications

### Strategy Analysis

- **Opening Ranges**: Analyze preflop hand selection
- **Betting Patterns**: Study postflop betting frequencies
- **Position Play**: Understand position-based strategy
- **Bluffing Frequency**: Analyze bluffing patterns

### Educational Research

- **Learning Effectiveness**: Measure how well students learn from AI explanations
- **Strategy Transfer**: Study how AI insights transfer to human play
- **Decision Quality**: Compare AI and human decision-making

### Technical Research

- **Interpretability vs Performance**: Trade-offs between transparency and accuracy
- **Feature Importance**: Which factors matter most in poker decisions
- **Tree Complexity**: Optimal balance between accuracy and interpretability

## 🔧 Customization

### Adding New Features

```python
# In feature_extractor.py
def extract_interpretable_features(state, player_id):
    features = {}
    # ... existing features ...
    
    # Add new feature
    features['custom_feature'] = calculate_custom_feature(state, player_id)
    
    return features
```

### Modifying Tree Parameters

```python
# In tree_trainer.py
trainer = InterpretableTreeTrainer(
    max_depth=15,           # Deeper trees
    min_samples_split=50,   # Fewer samples per split
    min_samples_leaf=25     # Fewer samples per leaf
)
```

### Custom Evaluation

```python
# Create custom evaluator
class CustomEvaluator(InterpretableEvaluator):
    def evaluate_custom_metric(self):
        # Custom evaluation logic
        pass
```

## 🐛 Troubleshooting

### Common Issues

1. **No trees found**: Ensure training data exists in `data/interpretable/`
2. **Import errors**: Check that all dependencies are installed
3. **Memory issues**: Reduce tree depth or use fewer features
4. **Performance issues**: Use fewer games for evaluation

### Debug Mode

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check tree statistics
trainer = InterpretableTreeTrainer()
summary = trainer.get_tree_summary()
print(summary)
```

## 📚 References

- Bertsimas, D., & Paskov, A. (2022). World-class interpretable poker. *Nature Machine Intelligence*.
- Deep CFR: Neural Network Counterfactual Regret Minimization
- Interpretable Machine Learning: A Guide for Making Black Box Models Explainable

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Original Deep CFR implementation
- Bertsimas & Paskov for interpretable poker research
- Poker community for strategy insights



