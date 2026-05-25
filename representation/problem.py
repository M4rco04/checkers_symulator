from typing import Dict, Tuple, List
from representation.board import Board
from representation.pawn import PawnColor, Pawn, PawnType
from representation.move import Move, Forward, Capture


class Problem:
    board: Board
    current_turn: PawnColor
    player_color: PawnColor

    def __init__(self, board: Board, player_color: PawnColor):
        self.board = board
        self.current_turn = PawnColor.White
        self.player_color = player_color

    def possible_moves(
        self, pawnColor: PawnColor, board: Board | None = None
    ) -> List[Move]:
        target_board: Board = board if board is not None else self.board
        possible_moves: List[Move] = []

        possible_moves_dict = self._possible_moves(pawnColor, target_board)

        for pawn_moves in possible_moves_dict.values():
            possible_moves.extend(pawn_moves)

        if any(isinstance(element, Capture) for element in possible_moves):
            possible_moves = list(
                filter(lambda element: isinstance(element, Capture), possible_moves)
            )

        return possible_moves

    def _find_all_captures(
        self,
        pawn: Pawn,
        current_pos: Tuple[int, int],
        captured_so_far: List[Pawn],
        board: Board,
    ) -> List[Capture]:
        captures = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        found_further_capture = False

        for dx, dy in directions:
            if pawn.type == PawnType.Knight:
                step = 1
                opponent_pawn = None

                while True:
                    check_x = current_pos[0] + step * dx
                    check_y = current_pos[1] + step * dy

                    if not (0 <= check_x <= 7 and 0 <= check_y <= 7):
                        break

                    occupant = board[(check_x, check_y)]

                    if occupant is None or occupant == pawn:
                        step += 1
                        continue
                    elif (
                        occupant.color == pawn.color.opposite()
                        and occupant not in captured_so_far
                    ):
                        opponent_pawn = occupant
                        break
                    else:
                        break

                if opponent_pawn is not None:
                    landing_step = step + 1
                    while True:
                        land_x = current_pos[0] + landing_step * dx
                        land_y = current_pos[1] + landing_step * dy

                        if not (0 <= land_x <= 7 and 0 <= land_y <= 7):
                            break

                        landing_occupant = board[(land_x, land_y)]

                        if landing_occupant is None or landing_occupant == pawn:
                            found_further_capture = True
                            new_captured = captured_so_far + [opponent_pawn]
                            landing_pos = (land_x, land_y)

                            further_captures = self._find_all_captures(
                                pawn, landing_pos, new_captured, board
                            )
                            captures.extend(further_captures)

                            landing_step += 1
                        else:
                            break

            else:
                opponent_pos = (current_pos[0] + dx, current_pos[1] + dy)
                landing_pos = (current_pos[0] + 2 * dx, current_pos[1] + 2 * dy)

                if 0 <= landing_pos[0] <= 7 and 0 <= landing_pos[1] <= 7:
                    opponent_pawn = board[opponent_pos]

                    if (
                        opponent_pawn is not None
                        and opponent_pawn.color == pawn.color.opposite()
                    ):
                        if opponent_pawn not in captured_so_far:
                            landing_occupant = board[landing_pos]

                            if landing_occupant is None or landing_occupant == pawn:
                                found_further_capture = True
                                new_captured = captured_so_far + [opponent_pawn]

                                further_captures = self._find_all_captures(
                                    pawn, landing_pos, new_captured, board
                                )
                                captures.extend(further_captures)

        if not found_further_capture and len(captured_so_far) > 0:
            captures.append(
                Capture(pawn.get_position(), current_pos, pawn, captured_so_far)
            )

        return captures

    def _possible_moves(
        self, pawnColor: PawnColor, board: Board
    ) -> Dict[Pawn, List[Move]]:
        moves: Dict[Pawn, List[Move]] = {}
        pawns = (
            board.white_pawns.values()
            if pawnColor == PawnColor.White
            else board.black_pawns.values()
        )

        for pawn in pawns:
            moves[pawn] = []
            position = pawn.get_position()

            captures = self._find_all_captures(pawn, position, [], board)
            if captures:
                moves[pawn].extend(captures)
                continue

            if pawn.type == PawnType.Knight:
                knight_moves = self._get_knight_moves(pawn, board)
                moves[pawn].extend(knight_moves)
            else:
                neighbors = pawn.neighborhood()
                for neighbor in neighbors:
                    if board[neighbor] is None and self._is_forward_move(
                        position, neighbor, pawn.color
                    ):
                        moves[pawn].append(Forward(position, neighbor, pawn))

        return moves

    def _is_forward_move(
        self, position: Tuple[int, int], move: Tuple[int, int], color: PawnColor
    ) -> bool:
        x = move[0] - position[0]
        if color == PawnColor.White:
            return x > 0
        else:
            return x < 0

    def _check_and_promote(self, pawn: Pawn) -> None:
        if pawn.color == PawnColor.White and pawn.x == 7:
            pawn.type = PawnType.Knight
        elif pawn.color == PawnColor.Black and pawn.x == 0:
            pawn.type = PawnType.Knight

    def _get_knight_moves(self, pawn: Pawn, board: Board) -> List[Move]:
        moves: List[Move] = []
        position = pawn.get_position()

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            for step in range(1, 8):
                new_x = position[0] + step * dx
                new_y = position[1] + step * dy

                if 0 <= new_x <= 7 and 0 <= new_y <= 7:
                    target_pos = (new_x, new_y)

                    if board[target_pos] is None:
                        moves.append(Forward(position, target_pos, pawn))
                    else:
                        break
                else:
                    break

        return moves

    def execute_move(self, move: Move, board: Board | None = None) -> None:
        target_board: Board = board if board is not None else self.board
        start = move.start
        to = move.to

        if isinstance(move, Capture):
            self.board.moves_without_capture = 0
        else:
            self.board.moves_without_capture += 1

        pawn_to_move = target_board[start]

        if pawn_to_move is None:
            return

        target_board[start] = None
        target_board[to] = pawn_to_move

        if pawn_to_move.color == PawnColor.White:
            del target_board.white_pawns[start]
            target_board.white_pawns[to] = pawn_to_move
        else:
            del target_board.black_pawns[start]
            target_board.black_pawns[to] = pawn_to_move

        pawn_to_move.x = to[0]
        pawn_to_move.y = to[1]

        if isinstance(move, Capture):
            if pawn_to_move.color == PawnColor.White:
                for captured_pawn in move.captured:
                    pos = captured_pawn.get_position()
                    if pos in target_board.black_pawns:
                        del target_board.black_pawns[pos]
                        target_board[pos] = None
            else:
                for captured_pawn in move.captured:
                    pos = captured_pawn.get_position()
                    if pos in target_board.white_pawns:
                        del target_board.white_pawns[pos]
                        target_board[pos] = None

        self._check_and_promote(pawn_to_move)

        if board is None:
            self.current_turn = self.current_turn.opposite()

    def simulate_move(self, board: Board, move: Move) -> Board:
        simulated_board = board.copy()
        self.execute_move(move, board=simulated_board)
        return simulated_board
