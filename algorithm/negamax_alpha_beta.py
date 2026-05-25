from datetime import datetime

from algorithm.algorithm import Algorithm
from representation.pawn import PawnColor
from representation.problem import Problem
from representation.move import Move
from representation.board import Board


class NegamaxAlphaBeta(Algorithm):
    def __init__(self, problem: Problem, color: PawnColor, timeout: float, depth: int):
        super().__init__(problem, color, timeout)
        self.depth = depth

    def make_move(self, move_number: int) -> Move | None:
        self.start = datetime.now()
        alpha = -float("inf")
        beta = float("inf")

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

            move_value = -self.negamax_alpha_beta(
                simulated_board, self.depth - 1, False, move_number, -beta, -alpha
            )

            if move_value > best_value:
                best_value = move_value
                best_move = move

            alpha = max(alpha, best_value)

        if best_move is None and possible_moves:
            best_move = possible_moves[0]

        return best_move

    def negamax_alpha_beta(
        self,
        board: Board,
        depth: int,
        is_our_turn: bool,
        move_number: int,
        alpha: float,
        beta: float,
    ) -> float:
        current_color = self.color if is_our_turn else self.color.opposite()

        if depth == 0 or self.is_terminal(current_color, board):
            eval_score = self.utility(board, move_number)
            return eval_score if is_our_turn else -eval_score

        if not self._any_time_left():
            eval_score = self.utility(board, move_number)
            return eval_score if is_our_turn else -eval_score

        max_value = -float("inf")

        for move in self.problem.possible_moves(current_color, board):
            new_board = self.problem.simulate_move(board, move)

            next_move = move_number + 1 if not is_our_turn else move_number

            value = -self.negamax_alpha_beta(
                new_board, depth - 1, not is_our_turn, next_move, -beta, -alpha
            )

            max_value = max(max_value, value)
            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return max_value
