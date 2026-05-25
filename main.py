from representation.board import Board
from representation.pawn import PawnColor
from representation.problem import Problem
from view.boardDrawer import BoardDrawer, Option

from algorithm.minmax import MinMax
from algorithm.negamax_alpha_beta import NegamaxAlphaBeta
from algorithm.iterative_deepening import IterativeDeepening


if __name__ == "__main__":
    player_color = PawnColor.White
    p = Problem(Board(pawn_rows=3), player_color)
    algorithm1 = MinMax(p, player_color, 3, 5)
    algorithm2 = NegamaxAlphaBeta(p, player_color.opposite(), 3, 5)
    algorithm3 = IterativeDeepening(p, player_color, 3, 10)
    drawer = BoardDrawer(Option.AIvAI, algorithm1=algorithm3, algorithm2=algorithm2)
    drawer.draw()
