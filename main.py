from representation.board import Board
from representation.pawn import PawnColor
from representation.problem import Problem
from view.boardDrawer import BoardDrawer, Option
from algorithm.minmax import MinMax


if __name__ == "__main__":
    player_color = PawnColor.White
    p = Problem(Board(pawn_rows=3), player_color)
    algorithm1 = MinMax(p, player_color, 10, 4)
    algorithm2 = MinMax(p, player_color.opposite(), 20, 2)
    drawer = BoardDrawer(Option.AIvAI, algorithm1=algorithm1, algorithm2=algorithm2)
    drawer.draw()
