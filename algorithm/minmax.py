from datetime import datetime

from algorithm.algorithm import Algorithm
from representation.pawn import PawnColor
from representation.problem import Problem
from representation.move import Move
from representation.board import Board


class MinMax(Algorithm):
    def __init__(self, problem: Problem, color: PawnColor, timeout: float, depth: int = 5):
        super().__init__(problem, color, timeout)
        self.depth = depth

    def make_move(self, move_number: int) -> Move | None:
        self.start = datetime.now()

        board = self.problem.board.copy()
        possible_moves = self.problem.possible_moves(self.color, board)

        if not possible_moves:
            return None
        possible_moves = self.order_moves(board, possible_moves, self.color)

        best_move = None
        best_value = -float("inf")

        for move in possible_moves:
            if not self._any_time_left():
                break

            simulated_board = self.problem.simulate_move(board, move)
            move_value = self.minmax(
                simulated_board, self.depth - 1, False, move_number
            )

            if move_value > best_value:
                best_value = move_value
                best_move = move

        if best_move is None and possible_moves:
            best_move = possible_moves[0]

        return best_move

    def minmax(
        self, board: Board, depth: int, maximizing_player: bool, move_number: int
    ) -> float:
        current_color = self.color if maximizing_player else self.color.opposite()

        if depth == 0 or self.is_terminal(current_color, board):
            return self.utility(board, move_number)

        if not self._any_time_left():
            return self.utility(board, move_number)

        if maximizing_player:
            max_eval = -float("inf")
            for move in self.problem.possible_moves(self.color, board):
                new_board = self.problem.simulate_move(board, move)
                eval_val = self.minmax(new_board, depth - 1, False, move_number)
                max_eval = max(max_eval, eval_val)
            return max_eval

        else:
            min_eval = float("inf")
            for move in self.problem.possible_moves(self.color.opposite(), board):
                new_board = self.problem.simulate_move(board, move)
                eval_val = self.minmax(new_board, depth - 1, True, move_number + 1)
                min_eval = min(min_eval, eval_val)
            return min_eval
