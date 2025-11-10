"""
Training script for interpretable poker AI.
Runs CFR training and collects decision data for interpretable agent training.
"""

import os
import sys
import argparse
import torch
import numpy as np
from typing import Dict, List, Any

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.core.deep_cfr import DeepCFRAgent
from src.interpretable.data_collector import InterpretableDataCollector, get_data_collector
from src.interpretable.feature_extractor import extract_interpretable_features
from src.training.train import train_deep_cfr
import pokers as pkrs

class InterpretableCFRAgent(DeepCFRAgent):
    """Deep CFR agent with data collection for interpretable training."""
    
    def __init__(self, player_id=0, num_players=6, memory_size=300000, device='cpu', 
                 data_collector=None):
        super().__init__(player_id, num_players, memory_size, device)
        self.data_collector = data_collector or get_data_collector()
        self.collect_data = True
    
    def cfr_traverse(self, state, iteration, random_agents, depth=0):
        """
        Modified CFR traversal with data collection.
        """
        # Add recursion depth protection
        max_depth = 1000
        if depth > max_depth:
            if hasattr(self, 'VERBOSE') and self.VERBOSE:
                print(f"WARNING: Max recursion depth reached ({max_depth}). Returning zero value.")
            return 0
        
        if state.final_state:
            # Return payoff for the trained agent
            return state.players_state[self.player_id].reward
        
        current_player = state.current_player
        
        # If it's the trained agent's turn
        if current_player == self.player_id:
            legal_action_types = self.get_legal_action_types(state)
            
            if not legal_action_types:
                if hasattr(self, 'VERBOSE') and self.VERBOSE:
                    print(f"WARNING: No legal actions found for player {current_player} at depth {depth}")
                return 0
            
            # Encode the base state
            state_tensor = torch.FloatTensor(self.encode_state(state, self.player_id)).to(self.device)
            
            # Get advantages and bet sizing prediction from network
            with torch.no_grad():
                advantages, bet_size_pred = self.advantage_net(state_tensor.unsqueeze(0))
                advantages = advantages[0].cpu().numpy()
                bet_size_multiplier = bet_size_pred[0][0].item()
            
            # Use regret matching to compute strategy for action types
            advantages_masked = np.zeros(self.num_actions)
            for a in legal_action_types:
                advantages_masked[a] = max(advantages[a], 0)
            
            # Choose an action based on the strategy
            if sum(advantages_masked) > 0:
                strategy = advantages_masked / sum(advantages_masked)
            else:
                strategy = np.zeros(self.num_actions)
                for a in legal_action_types:
                    strategy[a] = 1.0 / len(legal_action_types)
            
            # Choose actions and traverse
            action_values = np.zeros(self.num_actions)
            for action_type in legal_action_types:
                try:
                    # Use the predicted bet size for raise actions
                    if action_type == 2:  # Raise
                        pokers_action = self.action_type_to_pokers_action(action_type, state, bet_size_multiplier)
                    else:
                        pokers_action = self.action_type_to_pokers_action(action_type, state)
                    
                    new_state = state.apply_action(pokers_action)
                    
                    # Check if the action was valid
                    if new_state.status != pkrs.StateStatus.Ok:
                        continue  # Skip invalid actions
                    
                    action_values[action_type] = self.cfr_traverse(new_state, iteration, random_agents, depth + 1)
                except Exception as e:
                    if hasattr(self, 'VERBOSE') and self.VERBOSE:
                        print(f"ERROR in traversal for action {action_type}: {e}")
                    action_values[action_type] = 0
            
            # Compute counterfactual regrets and add to memory
            ev = sum(strategy[a] * action_values[a] for a in legal_action_types)
            
            # Calculate normalization factor
            max_abs_val = max(abs(max(action_values)), abs(min(action_values)), 1.0)
            
            for action_type in legal_action_types:
                # Calculate regret
                regret = action_values[action_type] - ev
                
                # Normalize and clip regret
                normalized_regret = regret / max_abs_val
                clipped_regret = np.clip(normalized_regret, -10.0, 10.0)
                
                # Apply scaling
                scale_factor = np.sqrt(iteration) if iteration > 1 else 1.0  # Linear CFR
                weighted_regret = clipped_regret * scale_factor
                
                # Store in prioritized memory with regret magnitude as priority
                priority = abs(weighted_regret) + 0.01  # Add small constant to ensure non-zero priority
                
                # For raise actions, store the bet size multiplier
                if action_type == 2:
                    self.advantage_memory.add(
                        (self.encode_state(state, self.player_id), 
                         np.zeros(20),  # placeholder for opponent features 
                         action_type, 
                         bet_size_multiplier, 
                         weighted_regret),
                        priority
                    )
                else:
                    self.advantage_memory.add(
                        (self.encode_state(state, self.player_id),
                         np.zeros(20),  # placeholder for opponent features
                         action_type, 
                         0.0,  # Default bet size for non-raise actions 
                         weighted_regret),
                        priority
                    )
            
            # Add to strategy memory
            strategy_full = np.zeros(self.num_actions)
            for a in legal_action_types:
                strategy_full[a] = strategy[a]
            
            self.strategy_memory.append((
                self.encode_state(state, self.player_id),
                np.zeros(20),  # placeholder for opponent features
                strategy_full,
                bet_size_multiplier if 2 in legal_action_types else 0.0,
                iteration
            ))
            
            # DATA COLLECTION: Record decision for interpretable training
            if self.collect_data and self.data_collector:
                # Choose the best action for data collection
                best_action_type = np.argmax(advantages_masked)
                if best_action_type == 2:  # Raise
                    best_action = self.action_type_to_pokers_action(best_action_type, state, bet_size_multiplier)
                else:
                    best_action = self.action_type_to_pokers_action(best_action_type, state)
                
                # Record the decision
                self.data_collector.record_decision(
                    state, self.player_id, best_action, action_values[best_action_type], iteration
                )
            
            return ev
            
        # If it's another player's turn (random agent)
        else:
            try:
                # Let the random agent choose an action
                action = random_agents[current_player].choose_action(state)
                new_state = state.apply_action(action)
                
                # Check if the action was valid
                if new_state.status != pkrs.StateStatus.Ok:
                    return 0
                
                return self.cfr_traverse(new_state, iteration, random_agents, depth + 1)
            except Exception as e:
                if hasattr(self, 'VERBOSE') and self.VERBOSE:
                    print(f"ERROR in random agent traversal: {e}")
                return 0
    
    def encode_state(self, state, player_id=0):
        """Encode state using the original encoding method."""
        from src.core.model import encode_state
        return encode_state(state, player_id)

def train_interpretable_cfr(num_iterations=1000, traversals_per_iteration=200, 
                          num_players=6, player_id=0, save_dir="models", 
                          log_dir="logs/interpretable_cfr", data_dir="data/interpretable",
                          verbose=False):
    """
    Train Deep CFR agent with data collection for interpretable agent.
    
    Args:
        num_iterations: Number of CFR iterations
        traversals_per_iteration: Number of traversals per iteration
        num_players: Number of players in the game
        player_id: ID of the player to train
        save_dir: Directory to save models
        log_dir: Directory for logs
        data_dir: Directory to save collected data
        verbose: Whether to print verbose output
    """
    print(f"Starting interpretable CFR training...")
    print(f"Iterations: {num_iterations}, Traversals: {traversals_per_iteration}")
    print(f"Data will be saved to: {data_dir}")
    
    # Create directories
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    
    # Initialize data collector
    data_collector = InterpretableDataCollector(data_dir)
    
    # Device configuration
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    # Initialize the interpretable CFR agent
    agent = InterpretableCFRAgent(
        player_id=player_id, 
        num_players=num_players, 
        device=device,
        data_collector=data_collector
    )
    
    # Training loop
    print("Starting training loop...")
    for iteration in range(num_iterations):
        if verbose and iteration % 100 == 0:
            print(f"Iteration {iteration}/{num_iterations}")
        
        # Run traversals for this iteration
        for traversal in range(traversals_per_iteration):
            # Create a new game state
            state = pkrs.State.from_seed(
                n_players=num_players,
                button=traversal % num_players,
                sb=1,
                bb=2,
                stake=200.0,
                seed=iteration * traversals_per_iteration + traversal
            )
            
            # Create random agents for opponents
            from src.agents.random_agent import RandomAgent
            random_agents = [RandomAgent(i) for i in range(num_players) if i != player_id]
            random_agents.insert(player_id, None)  # Insert None for the trained agent
            
            # Run CFR traversal
            agent.cfr_traverse(state, iteration + 1, random_agents)
        
        # Train networks periodically
        if iteration % 10 == 0 and iteration > 0:
            if len(agent.advantage_memory) > 128:
                agent.train_advantage_network()
            if len(agent.strategy_memory) > 128:
                agent.train_strategy_network()
        
        # Save data periodically
        if iteration % 100 == 0 and iteration > 0:
            data_collector.save_datasets()
            print(f"Saved data at iteration {iteration}")
    
    # Final data save
    data_collector.save_datasets()
    
    # Save the trained agent
    agent_path = os.path.join(save_dir, 'interpretable_cfr_agent.pt')
    agent.save_model(agent_path)
    print(f"Saved trained agent to {agent_path}")
    
    # Print collection statistics
    stats = data_collector.get_dataset_summary()
    print("\nData Collection Statistics:")
    print(f"Total decisions: {stats['total_decisions']}")
    print(f"Decisions by street: {stats['decisions_by_street']}")
    print(f"Actions taken: {stats['actions_taken']}")
    
    return agent, data_collector

def main():
    """Main training function."""
    parser = argparse.ArgumentParser(description='Train interpretable CFR agent')
    parser.add_argument('--iterations', type=int, default=1000, help='Number of CFR iterations')
    parser.add_argument('--traversals', type=int, default=200, help='Traversals per iteration')
    parser.add_argument('--save-dir', type=str, default='models', help='Directory to save models')
    parser.add_argument('--log-dir', type=str, default='logs/interpretable_cfr', help='Directory for logs')
    parser.add_argument('--data-dir', type=str, default='data/interpretable', help='Directory to save data')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Train the interpretable agent
    agent, data_collector = train_interpretable_cfr(
        num_iterations=args.iterations,
        traversals_per_iteration=args.traversals,
        save_dir=args.save_dir,
        log_dir=args.log_dir,
        data_dir=args.data_dir,
        verbose=args.verbose
    )
    
    print("Training completed successfully!")

if __name__ == "__main__":
    main()

