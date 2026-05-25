import math
import random
from datetime import datetime

from algorithm.algorithm import Algorithm
from representation.move import Move
from representation.problem import Problem
from representation.pawn import PawnColor
from heuristic.MCTSHeuristic import MCTSHeuristic


class MonteCarloSearchTree(Algorithm):
    n: int

    def __init__(self, problem: Problem, color: PawnColor, timeout: float, n: int):
        super().__init__(problem, color, timeout)
        self.n = n
        self.U = []
        self.N = []

        self.heuristic = MCTSHeuristic()

    def make_move(self, move_number: int) -> Move | None:
        self.start = datetime.now()

        board = self.problem.board.copy()
        possible_moves = self.problem.possible_moves(self.color, board)

        if not possible_moves:
            return None

        n = len(possible_moves)

        self.U = [0.0 for _ in range(n)]
        self.N = [1 for _ in range(n)]

        for _ in range(self.n):
            if not self._any_time_left():
                break

            best_i = 0
            best_ucb = -float('inf')

            for i in range(n):
                ucb_val = self.UCB1(i)
                if ucb_val > best_ucb:
                    best_ucb = ucb_val
                    best_i = i

            chosen_move = possible_moves[best_i]
            current_board = self.problem.simulate_move(board, chosen_move)

            current_turn = self.color.opposite()
            sim_move_number = move_number + 1
            current_depth = 0
            max_rollout_depth = 30

            while not self.is_terminal(current_turn, current_board) and current_depth < max_rollout_depth:
                rollout_moves = self.problem.possible_moves(current_turn, current_board)
                if not rollout_moves:
                    break

                random_move = random.choice(rollout_moves)
                current_board = self.problem.simulate_move(current_board, random_move)

                current_turn = current_turn.opposite()
                if current_turn == self.color:
                    sim_move_number += 1

                current_depth += 1

            score = self.utility(current_board, sim_move_number)

            self.U[best_i] += score
            self.N[best_i] += 1

        best_move_idx = self.N.index(max(self.N))

        return possible_moves[best_move_idx]

    def UCB1(self, i: int, c: float = 2 ** (1 / 2)) -> float:
        """
        Oblicza wartość UCB1 dla i-tego ruchu.
        """
        if self.N[i] == 0:
            return float('inf')

        total_visits = sum(self.N)

        exploitation = self.U[i] / self.N[i]
        exploration = c * math.sqrt(math.log(total_visits) / self.N[i])

        return exploitation + exploration