# Checkers AI Engine ♟️

An advanced checkers game engine written in Python. The project implements an object-oriented approach to game state representation and includes a suite of classic and modern artificial intelligence algorithms for selecting the best move.

## 🚀 Features and Algorithms

The project allows for pitting different AI algorithms against each other (AI vs AI) or playing a human player against the machine. The following decision-making algorithms have been implemented:

* **MinMax** – a classic game tree search algorithm.
* **Negamax with Alpha-Beta pruning** – an optimized version of the MinMax algorithm that significantly reduces the search space.
* **Iterative Deepening** – an *Anytime* algorithm that gradually increases the search depth, allowing calculations to be interrupted at any given moment (e.g., after a time limit expires) while retaining the best move found so far.
* **Monte Carlo Tree Search (MCTS)** – a heuristic algorithm based on random simulations (rollouts) that balances exploration and exploitation using the UCB1 formula.

## 🧠 Heuristics and Optimizations

* **Move Ordering:** The engine intelligently sorts possible moves before analyzing them, significantly speeding up Alpha-Beta pruning. It prioritizes captures, the creation of defensive chains, moving towards the edges, and promotions to kings.
* **Board evaluation:** The evaluation function takes into account not only the material balance (regular pawns and kings) but also the level of pawn advancement, safety (edge positions), and the time/number of moves to prevent prolonged games.
* **Draw handling:** A built-in 40-move rule without captures (preventing infinite loops in the endgame phase).

## 🛠️ Code Architecture

* `algorithm/` – implementations of the search algorithms.
* `heuristic/` – board state evaluation functions (classic and sigmoidal for MCTS).
* `representation/` – classes responsible for game logic and rules (`Board`, `Move`, `Pawn`, `Problem`). This includes the logic for multiple captures and the generation of legal moves.
* `view/` – the user interface (drawing the board).

## 💻 How to Run

To run the engine and start a game, execute the main file:

Two-player game:

```bash
python main.py -o PvP

```

Game against AI:

```bash
python main.py -o PvAI

```

AI vs AI game:

```bash
python main.py -o AIvAI

```

All configuration settings are located in the **settings.json** file.
