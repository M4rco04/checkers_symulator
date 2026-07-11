import os
import argparse
from sb3_contrib import MaskablePPO

from representation.board import Board
from representation.problem import Problem
from representation.pawn import PawnColor

from algorithm.reinforcement_learning import CheckersEngine
from algorithm.minmax import MinMax
from algorithm.negamax_alpha_beta import NegamaxAlphaBeta
from algorithm.iterative_deepening import IterativeDeepening
from algorithm.monte_carlo_search_tree import MonteCarloSearchTree

ALGORITHMS = {
    "MinMax": MinMax,
    "NegamaxAlphaBeta": NegamaxAlphaBeta,
    "IterativeDeepening": IterativeDeepening,
    "MCTS": MonteCarloSearchTree,
    "None": None
}

def main():
    parser = argparse.ArgumentParser(description="Program do nauki gry w warcaby reinforcement learning algorithm.")
    parser.add_argument(
        "-t", "--timesteps",
        required=True,
        type=int,
        help="Liczba akcji"
    )
    parser.add_argument(
        "-a", "--algorithm",
        choices=["MinMax", "NegamaxAlphaBeta", "IterativeDeepening", "MCTS"],
        help="Wybór algorytmu do nauki gry"
    )

    args = parser.parse_args()
    TIMESTEPS = args.timesteps

    board = Board(pawn_rows=3)
    color = PawnColor.White
    problem = Problem(board, color)

    if not args.algorithm:
        env = CheckersEngine(problem, opponent_algorithm=None)
    else:
        alg = ALGORITHMS[args.algorithm](problem, color.opposite(), timeout=0.05)
        env = CheckersEngine(problem, opponent_algorithm=alg)

    log_dir = "./checkers_tensorboard/"

    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, "maskable_ppo_checkers_model")
    model_file_path = f"{model_path}.zip"

    if os.path.exists(model_file_path):
        model = MaskablePPO.load(
            model_path,
            env=env,
            tensorboard_log=log_dir
        )
    else:
        model = MaskablePPO(
            "MlpPolicy",
            env,
            verbose=1,
            learning_rate=0.0003,
            tensorboard_log=log_dir
        )

    print(f"Rozpoczynam trening na {TIMESTEPS} kroków...")

    model.learn(
        total_timesteps=TIMESTEPS,
        reset_num_timesteps=False
    )

    model.save(model_path)
    print(f"Trening zakończony. Model zapisany jako: {model_file_path}")

if __name__ == "__main__":
    main()