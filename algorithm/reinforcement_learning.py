import gymnasium as gym
from gymnasium import spaces
import numpy as np
import numpy.typing as npt
import random
from typing import List

from representation.board import Board
from representation.pawn import PawnType, PawnColor
from representation.problem import Problem
from representation.move import Move
from heuristic.MCTSHeuristic import MCTSHeuristic
from algorithm.algorithm import Algorithm


class CheckersEngine(gym.Env):
    def __init__(self, problem: Problem, opponent_algorithm: Algorithm = None):
        super().__init__()
        self.problem = problem
        self.opponent_algorithm = opponent_algorithm

        self.heuristic = MCTSHeuristic()
        self.current_step = 0

        self.observation_space = spaces.Box(
            low=-2.0, high=2.0, shape=(64,), dtype=np.float32
        )

        self.action_space = spaces.Discrete(4096)

    def _change_board_into_tensor(self, board: Board) -> npt.NDArray[np.float32]:
        new_board = np.zeros((8, 8), dtype=np.float32)

        all_pawns = {**board.white_pawns, **board.black_pawns}

        for (x, y), pawn in all_pawns.items():
            if pawn.type == PawnType.Knight:
                new_board[x, y] = 2.0 if pawn.color == PawnColor.White else -2.0
            else:
                new_board[x, y] = 1.0 if pawn.color == PawnColor.White else -1.0

        return new_board.flatten()

    def _move_to_action(self, move: Move) -> int:
        start_x, start_y = move.start
        end_x, end_y = move.to

        from_square = start_x * 8 + start_y
        to_square = end_x * 8 + end_y

        return from_square * 64 + to_square

    def _action_to_move(self, action: int, legal_moves: List[Move]) -> Move:
        from_sq = action // 64
        to_sq = action % 64
        from_pos = (from_sq // 8, from_sq % 8)
        to_pos = (to_sq // 8, to_sq % 8)

        for move in legal_moves:
            if move.start == from_pos and move.to == to_pos:
                return move

    def action_masks(self) -> np.ndarray:
        masks = np.zeros(4096, dtype=bool)
        legal_moves = self.problem.possible_moves(self.problem.current_turn)

        for move in legal_moves:
            action_id = self._move_to_action(move)
            masks[action_id] = True

        return masks

    def _get_opponent_move(self, legal_moves: List[Move]) -> Move | None:
        if not legal_moves:
            return None

        if self.opponent_algorithm is not None:
            full_move_number = (self.current_step // 2) + 1
            return self.opponent_algorithm.make_move(full_move_number)

        return random.choice(legal_moves)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.problem.board = Board(pawn_rows=3)
        self.problem.current_turn = self.problem.player_color
        self.current_step = 0

        obs = self._change_board_into_tensor(self.problem.board)
        return obs, {}

    def step(self, action: int):
        self.current_step += 1

        terminated = False
        truncated = False
        reward = 0.0
        info = {}

        current_turn = self.problem.current_turn
        legal_moves = self.problem.possible_moves(current_turn)
        chosen_move = self._action_to_move(action, legal_moves)

        score_before = self.heuristic.evaluate(
            self.problem.board,
            self.problem.player_color,
            self.current_step
        )

        self.problem.execute_move(chosen_move)

        next_turn = self.problem.current_turn
        next_legal_moves = self.problem.possible_moves(next_turn)

        if self.problem.board.moves_without_capture >= 40:
            reward = 0.0
            terminated = True
        elif len(next_legal_moves) == 0:
            reward = 10.0
            terminated = True
        else:
            opponent_move = self._get_opponent_move(next_legal_moves)
            if opponent_move is not None:
                self.problem.execute_move(opponent_move)

            agent_legal_moves = self.problem.possible_moves(self.problem.current_turn)

            if self.problem.board.moves_without_capture >= 40:
                reward = 0.0
                terminated = True
            elif len(agent_legal_moves) == 0:
                reward = -10.0
                terminated = True
            else:
                score_after = self.heuristic.evaluate(
                    self.problem.board,
                    self.problem.player_color,
                    self.current_step
                )
                reward = score_after - score_before

        obs = self._change_board_into_tensor(self.problem.board)
        return obs, reward, terminated, truncated, info