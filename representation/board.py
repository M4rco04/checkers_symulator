from typing import Dict, Tuple
import numpy as np
import numpy.typing as npt

from representation.pawn import Pawn, PawnColor


class Board:
    board: npt.NDArray[None | Pawn]

    white_pawns: Dict[Tuple[int, int], Pawn]
    black_pawns: Dict[Tuple[int, int], Pawn]
    moves_without_capture: int

    def __init__(self, pawn_rows: int):
        self.moves_without_capture = 0
        self.white_pawns = dict()
        self.black_pawns = dict()
        self.board = np.full((8, 8), None, dtype=object)

        for i in range(pawn_rows):
            for j in range(0, 8, 2):
                white_pawn = self._create_white_pawn(i, j)
                black_pawn = self._create_black_pawn(i, j)

                self.board[white_pawn.get_position()] = white_pawn
                self.board[black_pawn.get_position()] = black_pawn

                self.white_pawns[white_pawn.get_position()] = white_pawn
                self.black_pawns[black_pawn.get_position()] = black_pawn

    def _create_white_pawn(self, i: int, j: int) -> Pawn:
        x = i
        if i % 2 == 0:
            y = j
        else:
            y = j + 1
        return Pawn(x, y, PawnColor.White)

    def _create_black_pawn(self, i: int, j: int) -> Pawn:
        x = 8 - i - 1
        if i % 2 == 0:
            y = j + 1
        else:
            y = j
        return Pawn(x, y, PawnColor.Black)

    def __getitem__(self, pos: Tuple[int, int]) -> Pawn | None:
        return self.board[pos]

    def __setitem__(self, pos: Tuple[int, int], value: Pawn | None):
        self.board[pos] = value

    def copy(self) -> "Board":
        new_board = Board(0)

        for pos, pawn in self.white_pawns.items():
            new_pawn = Pawn(pawn.x, pawn.y, pawn.color)
            new_pawn.type = pawn.type
            new_board.board[pos] = new_pawn
            new_board.white_pawns[pos] = new_pawn

        for pos, pawn in self.black_pawns.items():
            new_pawn = Pawn(pawn.x, pawn.y, pawn.color)
            new_pawn.type = pawn.type
            new_board.board[pos] = new_pawn
            new_board.black_pawns[pos] = new_pawn

        new_board.moves_without_capture = self.moves_without_capture
        return new_board
