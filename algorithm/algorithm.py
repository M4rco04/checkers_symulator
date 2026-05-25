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
        moves = self.problem.possible_moves(color, board)
        return len(moves) == 0

    def utility(self, board: Board, move_number: int) -> float:
        return self.heuristic.evaluate(board, self.color, move_number)