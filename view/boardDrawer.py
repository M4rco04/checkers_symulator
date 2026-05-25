import copy
from enum import Enum
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.widgets import Button

from representation.pawn import PawnColor, PawnType


class Option(Enum):
    PvP = 0
    PvAI = 1
    AIvAI = 2


class BoardDrawer:
    player_color: PawnColor = None

    def __init__(self, option: Option, **kwargs):
        """
        Inicjalizuje obiekt rysujący planszę, ustawia paletę kolorów,
        perspektywę gracza oraz początkowy stan historii gry.
        """
        self.option = option

        if option == Option.PvP:
            self.problem = kwargs["problem"]
            self.player_color = kwargs.get("player_color", PawnColor.White)
        elif option == Option.PvAI:
            self.algorithm = kwargs["algorithm"]
            self.problem = self.algorithm.problem
            self.player_color = kwargs.get("player_color", PawnColor.White)
        elif option == Option.AIvAI:
            self.algorithm1 = kwargs["algorithm1"]
            self.algorithm2 = kwargs["algorithm2"]
            self.problem = self.algorithm1.problem
            self.player_color = PawnColor.White
        else:
            raise ValueError("Brak takiej opcji")

        self._checker_cmap = ListedColormap(["#f0d9b5", "#b58863"])
        self._pawn_white_color = "white"
        self._pawn_black_color = "#333333"
        self._pawn_edge_white = "black"
        self._pawn_edge_black = "white"
        self._knight_star_color = "gold"

        self._btn_color = "#b58863"
        self._btn_hover_color = "#f0d9b5"
        self._btn_edge_color = "#333333"

        self.selected_pawn = None
        self.valid_moves_for_selected = {}

        self.history = [copy.deepcopy(self.problem.board)]
        self.history_index = 0

    @property
    def current_full_move(self) -> int:
        """
        Zwraca aktualny numer pełnego ruchu w grze.
        1 - ruch białych i czarnych, 2 - kolejny ruch białych i czarnych itd.
        """
        return (self.history_index // 2) + 1

    def _map_row(self, x: int) -> int:
        """
        Mapuje logiczny indeks wiersza na współrzędną osi Y na wykresie,
        uwzględniając to, którym kolorem gra użytkownik.
        """
        if self.player_color is None or self.player_color == PawnColor.White:
            return 7 - x
        return x

    def _unmap_row(self, y_visual: float) -> int:
        """
        Przekształca wizualną współrzędną Y z kliknięcia myszką z powrotem
        na logiczny indeks wiersza w reprezentacji planszy.
        """
        y_vis_int = int(round(y_visual))
        if self.player_color == PawnColor.White:
            return 7 - y_vis_int
        return y_vis_int

    def on_click(self, event):
        """
        Obsługuje kliknięcia myszką: zaznaczanie pionków, podświetlanie
        możliwych ruchów oraz wykonywanie ruchu na planszy.
        """
        if event.inaxes != self.ax:
            return
        if event.xdata is None or event.ydata is None:
            return

        if self.history_index < len(self.history) - 1:
            return

        is_human_turn = False
        if self.option == Option.PvP:
            is_human_turn = True
        elif self.option == Option.PvAI:
            is_human_turn = self.problem.current_turn == self.player_color

        if not is_human_turn:
            return

        col = int(round(event.xdata))
        row = self._unmap_row(event.ydata)
        dest = (row, col)

        if not (0 <= row <= 7 and 0 <= col <= 7):
            return

        if self.selected_pawn is not None and dest in self.valid_moves_for_selected:
            move = self.valid_moves_for_selected[dest]

            self.problem.execute_move(move)
            self.history.append(copy.deepcopy(self.problem.board))
            self.history_index += 1

            self.selected_pawn = None
            self.valid_moves_for_selected.clear()

            self._redraw()

            self.handle_computer_move()
            return

        board = self.problem.board
        pawn = board[dest]

        if pawn is not None and pawn.color == self.problem.current_turn:
            self.selected_pawn = pawn
            self.valid_moves_for_selected.clear()

            all_valid_moves = self.problem.possible_moves(self.problem.current_turn)
            for move in all_valid_moves:
                if move.pawn == pawn:
                    self.valid_moves_for_selected[move.to] = move
        else:
            self.selected_pawn = None
            self.valid_moves_for_selected.clear()

        self._redraw()

    def on_key_press(self, event):
        if event.key == "left":
            self.go_prev(None)
        elif event.key == "right":
            self.go_next(None)

    def go_to_start(self, event):
        if self.history_index > 0:
            self.history_index = 0
            self.selected_pawn = None
            self.valid_moves_for_selected.clear()
            self._redraw()

    def go_prev(self, event):
        if self.history_index > 0:
            self.history_index -= 1
            self.selected_pawn = None
            self.valid_moves_for_selected.clear()
            self._redraw()

    def go_next(self, event):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.selected_pawn = None
            self.valid_moves_for_selected.clear()
            self._redraw()

    def go_to_end(self, event):
        if self.history_index < len(self.history) - 1:
            self.history_index = len(self.history) - 1
            self.selected_pawn = None
            self.valid_moves_for_selected.clear()
            self._redraw()

    def _redraw(self):
        """
        Czyści aktualny wykres i rysuje od nowa szachownicę, pionki
        oraz ewentualne podświetlenia możliwych ruchów na podstawie historii.
        """
        self.ax.clear()
        board_to_draw = self.history[self.history_index]

        checkerboard = np.zeros((8, 8))
        checkerboard[1::2, ::2] = 1
        checkerboard[::2, 1::2] = 1

        grid_to_plot = checkerboard
        if self.player_color == PawnColor.White:
            grid_to_plot = np.flipud(checkerboard)

        self.ax.imshow(grid_to_plot, cmap=self._checker_cmap, origin="upper")

        all_pawns = {**board_to_draw.white_pawns, **board_to_draw.black_pawns}

        for (x, y), pawn in all_pawns.items():
            p_color = (
                self._pawn_white_color
                if pawn.color == PawnColor.White
                else self._pawn_black_color
            )
            e_color = (
                self._pawn_edge_white
                if pawn.color == PawnColor.White
                else self._pawn_edge_black
            )

            y_visual = self._map_row(x)

            self.ax.plot(
                y,
                y_visual,
                "o",
                markersize=32,
                color=p_color,
                markeredgecolor=e_color,
                markeredgewidth=2,
            )

            if (
                self.selected_pawn
                and pawn.get_position() == self.selected_pawn.get_position()
            ):
                self.ax.plot(
                    y,
                    y_visual,
                    "o",
                    markersize=32,
                    color="none",
                    markeredgecolor="red",
                    markeredgewidth=3,
                )

            if pawn.type == PawnType.Knight:
                self.ax.plot(
                    y, y_visual, "*", markersize=14, color=self._knight_star_color
                )

        for dest, move in self.valid_moves_for_selected.items():
            vis_dest_x = self._map_row(dest[0])
            self.ax.plot(
                dest[1], vis_dest_x, "o", markersize=18, color="green", alpha=0.5
            )

        self.ax.set_xticks(np.arange(8))
        self.ax.set_yticks(np.arange(8))
        self.ax.set_xticklabels(["A", "B", "C", "D", "E", "F", "G", "H"])
        self.ax.xaxis.tick_top()

        labels_y = ["1", "2", "3", "4", "5", "6", "7", "8"]
        if self.player_color == PawnColor.White:
            labels_y = list(reversed(labels_y))

        self.ax.set_yticklabels(labels_y)
        self.ax.grid(False)

        if self.history_index < len(self.history) - 1:
            self.ax.set_title(
                f"HISTORIA (Ruch: {self.current_full_move})",
                color="#b58863",
                fontsize=14,
                fontweight="bold",
                loc="center",
            )
        else:
            current_turn = self.problem.current_turn
            possible_moves = self.problem.possible_moves(current_turn)

            if len(possible_moves) == 0:
                zwyciezca = "Białe" if current_turn == PawnColor.Black else "Czarne"
                self.ax.set_title(
                    f"KONIEC GRY! Wygrały: {zwyciezca}",
                    fontsize=16,
                    fontweight="bold",
                    color="red",
                    loc="center",
                )
            else:
                tura = "Białe" if current_turn == PawnColor.White else "Czarne"
                self.ax.set_title(
                    f"Tura: {tura}", fontsize=16, fontweight="bold", loc="center"
                )

        self.fig.canvas.draw()

    def handle_computer_move(self):
        """
        Pauzuje na chwilę grę, pobiera ruch od komputera i wykonuje go na planszy.
        Obsługuje zarówno pojedynczy ruch dla trybu PvAI, jak i cykliczne ruchy dla AIvAI.
        """
        while True:
            current_turn = self.problem.current_turn

            if len(self.problem.possible_moves(current_turn)) == 0:
                break

            active_algo = None
            if self.option == Option.PvAI and current_turn != self.player_color:
                active_algo = self.algorithm
            elif self.option == Option.AIvAI:
                if self.algorithm1.color == current_turn:
                    active_algo = self.algorithm1
                else:
                    active_algo = self.algorithm2

            if active_algo is None:
                break

            plt.pause(0.5)
            computer_move = active_algo.make_move(self.current_full_move)

            if computer_move is not None:
                self.problem.execute_move(computer_move)
                self.history.append(copy.deepcopy(self.problem.board))
                self.history_index += 1
                self.selected_pawn = None
                self.valid_moves_for_selected.clear()
                self._redraw()
            else:
                break

    def draw(self):
        """
        Przygotowuje okno Matplotlib, ustawia układy współrzędnych,
        podpina przyciski sterujące oraz zdarzenia, a następnie renderuje planszę.
        """
        self.fig, self.ax = plt.subplots(figsize=(8, 8))

        plt.subplots_adjust(bottom=0.12)

        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.fig.canvas.mpl_connect("key_press_event", self.on_key_press)

        ax_start = plt.axes([0.31, 0.02, 0.08, 0.06], frame_on=True)
        ax_prev = plt.axes([0.41, 0.02, 0.08, 0.06], frame_on=True)
        ax_next = plt.axes([0.51, 0.02, 0.08, 0.06], frame_on=True)
        ax_end = plt.axes([0.61, 0.02, 0.08, 0.06], frame_on=True)

        self.btn_start = Button(
            ax_start, "◀◀", color=self._btn_color, hovercolor=self._btn_hover_color
        )
        self.btn_prev = Button(
            ax_prev, "◀", color=self._btn_color, hovercolor=self._btn_hover_color
        )
        self.btn_next = Button(
            ax_next, "▶", color=self._btn_color, hovercolor=self._btn_hover_color
        )
        self.btn_end = Button(
            ax_end, "▶▶", color=self._btn_color, hovercolor=self._btn_hover_color
        )

        for btn, ax in zip(
            [self.btn_start, self.btn_prev, self.btn_next, self.btn_end],
            [ax_start, ax_prev, ax_next, ax_end],
        ):
            btn.label.set_fontsize(18)
            ax.spines["top"].set_edgecolor(self._btn_edge_color)
            ax.spines["bottom"].set_edgecolor(self._btn_edge_color)
            ax.spines["left"].set_edgecolor(self._btn_edge_color)
            ax.spines["right"].set_edgecolor(self._btn_edge_color)

        self.btn_start.on_clicked(self.go_to_start)
        self.btn_prev.on_clicked(self.go_prev)
        self.btn_next.on_clicked(self.go_next)
        self.btn_end.on_clicked(self.go_to_end)

        self._redraw()

        self.handle_computer_move()

        plt.show()
