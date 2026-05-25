import argparse
import json
import sys
from representation.board import Board
from representation.pawn import PawnColor
from representation.problem import Problem
from view.boardDrawer import BoardDrawer, Option

from algorithm.minmax import MinMax
from algorithm.negamax_alpha_beta import NegamaxAlphaBeta
from algorithm.iterative_deepening import IterativeDeepening
from algorithm.monte_carlo_search_tree import MonteCarloSearchTree

ALGORITHMS = {
    "MinMax": MinMax,
    "NegamaxAlphaBeta": NegamaxAlphaBeta,
    "IterativeDeepening": IterativeDeepening,
    "MCTS": MonteCarloSearchTree
}


def load_config(config_path):
    """Wczytuje konfigurację z pliku JSON."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku konfiguracyjnego '{config_path}'", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Błąd: Plik '{config_path}' nie jest poprawnym plikiem JSON", file=sys.stderr)
        sys.exit(1)


def create_algorithm(name, problem, color, config):
    """Dynamicznie tworzy instancję algorytmu na podstawie konfiguracji."""
    if name not in ALGORITHMS:
        raise ValueError(f"Nieznany algorytm: {name}. Dostępne: {list(ALGORITHMS.keys())}")

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

    args = parser.parse_args()

    config = load_config(args.config)
    pawn_rows = config.get("rows", 3)

    board = Board(pawn_rows=pawn_rows)
    algorithm1 = None
    algorithm2 = None

    try:
        option_enum = Option[args.option]
    except KeyError:
        print(f"Błąd: Opcja {args.option} nie pasuje do wewnętrznych opcji gry.", file=sys.stderr)
        sys.exit(1)

    if args.option == "PvP":
        player_color_val = config["PvP"]["player_color"]
        player_color = PawnColor(player_color_val)  # 0 dla Black, 1 dla White
        p = Problem(board, player_color)

    elif args.option == "PvAI":
        player_color_val = config["PvAI"]["player_color"]
        player_color = PawnColor(player_color_val)
        p = Problem(board, player_color)

        ai_color = player_color.opposite()
        algo_name = config["PvAI"]["algorithm"]
        algorithm1 = create_algorithm(algo_name, p, ai_color, config)

    elif args.option == "AIvAI":
        player_color = PawnColor.White
        p = Problem(board, player_color)

        algo1_name = config["AIvAI"]["algorithm1"]
        algo2_name = config["AIvAI"]["algorithm2"]

        algorithm1 = create_algorithm(algo1_name, p, PawnColor.White, config)
        algorithm2 = create_algorithm(algo2_name, p, PawnColor.Black, config)

    drawer = BoardDrawer(option_enum, algorithm1=algorithm1, algorithm2=algorithm2)
    drawer.draw()


if __name__ == "__main__":
    main()