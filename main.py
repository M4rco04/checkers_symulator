import argparse
import json
import numpy as np

from representation.board import Board
from representation.pawn import PawnColor, PawnType
from representation.problem import Problem
from view.boardDrawer import BoardDrawer, Option

from algorithm.minmax import MinMax
from algorithm.negamax_alpha_beta import NegamaxAlphaBeta
from algorithm.iterative_deepening import IterativeDeepening
from algorithm.monte_carlo_search_tree import MonteCarloSearchTree
from algorithm .algorithm import Algorithm

from sb3_contrib import MaskablePPO

ALGORITHMS = {
    "MinMax": MinMax,
    "NegamaxAlphaBeta": NegamaxAlphaBeta,
    "IterativeDeepening": IterativeDeepening,
    "MCTS": MonteCarloSearchTree
}

DEFAULT_MODEL_PATH = "models/maskable_ppo_checkers_model"


class PPOAgent(Algorithm):
    def __init__(self, problem: Problem, color: PawnColor, model_path: str):
        super().__init__(problem, color, timeout=0.0)
        self.model = MaskablePPO.load(model_path)

    def _change_board_into_tensor(self, board: Board):
        new_board = np.zeros((8, 8), dtype=np.float32)
        all_pawns = {**board.white_pawns, **board.black_pawns}

        for (x, y), pawn in all_pawns.items():
            if pawn.type == PawnType.Knight:
                new_board[x, y] = 2.0 if pawn.color == PawnColor.White else -2.0
            else:
                new_board[x, y] = 1.0 if pawn.color == PawnColor.White else -1.0

        return new_board.flatten()

    def make_move(self, move_number: int):
        obs = self._change_board_into_tensor(self.problem.board)
        legal_moves = self.problem.possible_moves(self.color)

        masks = np.zeros(4096, dtype=bool)
        for move in legal_moves:
            from_sq = move.start[0] * 8 + move.start[1]
            to_sq = move.to[0] * 8 + move.to[1]
            masks[from_sq * 64 + to_sq] = True

        action, _states = self.model.predict(obs, action_masks=masks, deterministic=True)

        from_sq = int(action) // 64
        to_sq = int(action) % 64
        from_pos = (from_sq // 8, from_sq % 8)
        to_pos = (to_sq // 8, to_sq % 8)

        for move in legal_moves:
            if move.start == from_pos and move.to == to_pos:
                return move

        return None


def load_config(config_path):
    """Wczytuje konfigurację z pliku JSON."""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_algorithm(name, problem, color, config):
    """Dynamicznie tworzy instancję algorytmu na podstawie konfiguracji."""
    algo_class = ALGORITHMS[name]
    algo_params = config.get(name, {})
    timeout = algo_params.get("timeout", 3.0)

    if name == "MCTS":
        n = algo_params.get("n", 100000)
        return algo_class(problem, color, timeout, n)
    else:
        depth = algo_params.get("depth", 5)
        return algo_class(problem, color, timeout, depth)


def main():
    parser = argparse.ArgumentParser(description="Silnik gry w warcaby z obsługą AI.")
    parser.add_argument(
        "-o", "--option",
        choices=["PvP", "PvAI", "AIvAI"],
        required=True,
        help="Wybór trybu gry: PvP (Gracz vs Gracz), PvAI (Gracz vs AI), AIvAI (AI vs AI)"
    )
    parser.add_argument(
        "-c", "--config",
        default="settings.json",
        help="Ścieżka do pliku konfiguracyjnego JSON (domyślnie: config.json)"
    )
    parser.add_argument(
        "-r", "--reinforcement",
        choices=["Black", "White"],
        help="Wykorzystanie modelu nauczonego przez wzmacnianie"
    )

    args = parser.parse_args()

    config = load_config(args.config)
    pawn_rows = config.get("rows", 3)

    board = Board(pawn_rows=pawn_rows)
    algorithm1 = None
    algorithm2 = None

    option_enum = Option[args.option]

    if args.option == "PvP":
        player_color_val = config["PvP"]["player_color"]
        player_color = PawnColor(player_color_val)
        p = Problem(board, player_color)

    elif args.option == "PvAI":
        if args.reinforcement:
            player_color_val = 0 if args.reinforcement == "White" else 1
        else:
            player_color_val = config["PvAI"]["player_color"]

        player_color = PawnColor(player_color_val)
        p = Problem(board, player_color)

        ai_color = player_color.opposite()

        if args.reinforcement:
            algorithm1 = PPOAgent(p, ai_color, DEFAULT_MODEL_PATH)
        else:
            algo_name = config["PvAI"]["algorithm"]
            algorithm1 = create_algorithm(algo_name, p, ai_color, config)

    elif args.option == "AIvAI":
        player_color = PawnColor.White
        p = Problem(board, player_color)

        if args.reinforcement:
            if args.reinforcement == "White":
                algorithm1 = PPOAgent(p, PawnColor.White, DEFAULT_MODEL_PATH)
                algorithm2 = create_algorithm(config["AIvAI"]["algorithm2"], p, PawnColor.Black, config)
            else:
                algorithm1 = create_algorithm(config["AIvAI"]["algorithm1"], p, PawnColor.White, config)
                algorithm2 = PPOAgent(p, PawnColor.Black, DEFAULT_MODEL_PATH)
        else:
            algo1_name = config["AIvAI"]["algorithm1"]
            algo2_name = config["AIvAI"]["algorithm2"]
            algorithm1 = create_algorithm(algo1_name, p, PawnColor.White, config)
            algorithm2 = create_algorithm(algo2_name, p, PawnColor.Black, config)

    drawer = BoardDrawer(option_enum, algorithm1=algorithm1, algorithm2=algorithm2, problem=p, player_color=player_color)
    drawer.draw()


if __name__ == "__main__":
    main()