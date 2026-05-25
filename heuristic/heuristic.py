from representation.board import Board
from representation.pawn import PawnColor, PawnType


class Heuristic:
    def __init__(self):
        self.PAWN_VALUE = 10
        self.KNIGHT_VALUE = 30

        self.ADVANCEMENT_MULTIPLIER = 0.3
        self.EDGE_BONUS = 0.5
        self.CHAIN_BONUS = 0.2

        self.alpha = 0.1

    def evaluate(self, board: Board, maximizing_color: PawnColor, move: int) -> float:
        white_score = self._evaluate_color(board, PawnColor.White)
        black_score = self._evaluate_color(board, PawnColor.Black)

        time_penalty = self.alpha * move

        if maximizing_color == PawnColor.White:
            return white_score - black_score - time_penalty
        else:
            return black_score - white_score - time_penalty

    def _evaluate_color(self, board: Board, color: PawnColor) -> float:
        score = 0.0

        pawns_dict = (
            board.white_pawns if color == PawnColor.White else board.black_pawns
        )
        pawns = pawns_dict.values()

        if len(pawns) == 0:
            return -float("inf")

        for pawn in pawns:
            if pawn.type == PawnType.Knight:
                score += self.KNIGHT_VALUE
            else:
                score += self.PAWN_VALUE

                if color == PawnColor.White:
                    score += pawn.x * self.ADVANCEMENT_MULTIPLIER
                else:
                    score += (7 - pawn.x) * self.ADVANCEMENT_MULTIPLIER

            if pawn.y == 0 or pawn.y == 7:
                score += self.EDGE_BONUS

            if color == PawnColor.White:
                if (pawn.x - 1, pawn.y - 1) in pawns_dict:
                    score += self.CHAIN_BONUS
                if (pawn.x - 1, pawn.y + 1) in pawns_dict:
                    score += self.CHAIN_BONUS
            else:
                if (pawn.x + 1, pawn.y - 1) in pawns_dict:
                    score += self.CHAIN_BONUS
                if (pawn.x + 1, pawn.y + 1) in pawns_dict:
                    score += self.CHAIN_BONUS

        return score
