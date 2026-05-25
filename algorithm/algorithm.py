from abc import ABC, abstractmethod
from datetime import datetime

from heuristic.heuristic import Heuristic
from representation.move import Move
from representation.problem import Problem
from representation.pawn import PawnColor
from representation.board import Board


class Algorithm(ABC):
    problem: Problem
    start: datetime
    timeout: float

    def __init__(self, problem: Problem, color: PawnColor, timeout: float):
        self.problem = problem
        self.color = color
        self.timeout = timeout
        self.heuristic = Heuristic()

    def _any_time_left(self) -> bool:
        return (datetime.now() - self.start).total_seconds() < self.timeout

    @abstractmethod
    def make_move(self, move_number: int) -> Move | None:
        pass

    def is_terminal(self, color: PawnColor, board: Board) -> bool:
        if board.moves_without_capture >= 40:
            return True

        moves = self.problem.possible_moves(color, board)
        return len(moves) == 0

    def utility(self, board: Board, move_number: int) -> float:
        if board.moves_without_capture >= 40:
            return 0.0

        return self.heuristic.evaluate(board, self.color, move_number)

    def order_moves(
        self, board: Board, moves: list[Move], color: PawnColor
    ) -> list[Move]:
        """
        Sortuje listę możliwych ruchów od najbardziej obiecujących do najmniej
        """

        def move_score(move: Move) -> float:
            score = 0.0
            dest_x, dest_y = move.to

            target_pawn = board[move.to]
            if target_pawn is not None and target_pawn.color != color:
                score += 1000.0

            if color == PawnColor.White and dest_x == 7:
                score += 500.0
            elif color == PawnColor.Black and dest_x == 0:
                score += 500.0

            pawns_dict = (
                board.white_pawns if color == PawnColor.White else board.black_pawns
            )
            if color == PawnColor.White:
                if (dest_x - 1, dest_y - 1) in pawns_dict or (
                    dest_x - 1,
                    dest_y + 1,
                ) in pawns_dict:
                    score += 200.0
            else:
                if (dest_x + 1, dest_y - 1) in pawns_dict or (
                    dest_x + 1,
                    dest_y + 1,
                ) in pawns_dict:
                    score += 200.0

            if dest_y == 0 or dest_y == 7:
                score += 50.0

            if color == PawnColor.White:
                score += dest_x * 5.0
            else:
                score += (7 - dest_x) * 5.0

            return score

        return sorted(moves, key=move_score, reverse=True)
