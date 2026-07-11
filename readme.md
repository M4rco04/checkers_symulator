# Checkers AI Engine ♟️

An advanced checkers game engine written in Python. The project implements an object-oriented approach to game state representation and includes a suite of classic, modern, and machine learning artificial intelligence algorithms for selecting the best move.

## 🚀 Features and Algorithms

The project allows for pitting different AI algorithms against each other (AI vs AI) or playing a human player against the machine. The following decision-making algorithms have been implemented:

- **MinMax** – a classic game tree search algorithm.
- **Negamax with Alpha-Beta pruning** – an optimized version of the MinMax algorithm that significantly reduces the search space.
- **Iterative Deepening** – an *Anytime* algorithm that gradually increases the search depth, allowing calculations to be interrupted at any given moment (e.g., after a time limit expires) while retaining the best move found so far.
- **Monte Carlo Tree Search (MCTS)** – a heuristic algorithm based on random simulations (rollouts) that balances exploration and exploitation using the UCB1 formula.
- **Reinforcement Learning (Maskable PPO)** – a neural network agent trained using Proximal Policy Optimization from the `sb3-contrib` library. It utilizes Action Masking to strictly enforce legal moves and learns through interaction with a custom Gymnasium environment.

## 🧠 Heuristics and Optimizations

- **Move Ordering:** The engine intelligently sorts possible moves before analyzing them, significantly speeding up Alpha-Beta pruning. It prioritizes captures, the creation of defensive chains, moving towards the edges, and promotions to kings.
- **Board Evaluation:** The evaluation function takes into account not only the material balance (regular pawns and kings) but also the level of pawn advancement, safety (edge positions), and the time/number of moves to prevent prolonged games.
- **Draw Handling:** A built-in 40-move rule without captures, preventing infinite loops in the endgame.

## 🛠️ Code Architecture

- `algorithm/` – implementations of the search algorithms and the custom Gymnasium environment (`CheckersEngine`).
- `heuristic/` – board state evaluation functions (classic and sigmoidal for MCTS).
- `representation/` – classes responsible for game logic and rules (`Board`, `Move`, `Pawn`, `Problem`), including multiple captures and legal move generation.
- `view/` – graphical user interface and board rendering.
- `reinforcement.py` – script for training the reinforcement learning agent.

## 💻 How to Run

### Playing the Game

To run the engine and start a game, execute `main.py`.

#### Two-player game

```bash
python main.py -o PvP
```

#### Play against the classical AI (configured in `settings.json`)

```bash
python main.py -o PvAI
```

#### AI vs AI

```bash
python main.py -o AIvAI
```

#### Play against the Reinforcement Learning agent

You can use the trained RL model in both `PvAI` and `AIvAI` modes by specifying the `-r` flag followed by the color controlled by the RL agent (`White` or `Black`).

```bash
python main.py -o PvAI -r Black
```

### Training the Reinforcement Learning Agent

To train the Maskable PPO agent, run `reinforcement.py`.

The number of training timesteps must be specified with the `-t` flag. Optionally, you can choose the opponent algorithm using the `-a` flag.

#### Train against a random opponent (100,000 timesteps)

```bash
python reinforcement.py -t 100000
```

#### Train against MinMax (500,000 timesteps)

```bash
python reinforcement.py -t 500000 -a MinMax
```