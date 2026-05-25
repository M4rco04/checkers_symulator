import math
from heuristic.heuristic import Heuristic
from representation.board import Board
from representation.pawn import PawnColor


class MCTSHeuristic:
    def __init__(self):
        self.base_heuristic = Heuristic()

        self.k = 0.05

    def evaluate(self, board: Board, maximizing_color: PawnColor, move: int) -> float:
        """
        Zwraca znormalizowaną ocenę planszy w przedziale (0, 1) na potrzeby MCTS.
        """
        raw_score = self.base_heuristic.evaluate(board, maximizing_color, move)

        if raw_score == float('inf'):
            return 1.0
        if raw_score == -float('inf'):
            return 0.0

        probability = 1.0 / (1.0 + math.exp(-self.k * raw_score))

        return probability