from abc import ABC
from typing import Tuple, List

from representation.pawn import Pawn


class Move(ABC):
    start: Tuple[int, int]
    to: Tuple[int, int]
    pawn: Pawn


class Capture(Move):
    captured: List[Pawn]

    def __init__(
        self,
        start: Tuple[int, int],
        to: Tuple[int, int],
        pawn: Pawn,
        captured: List[Pawn],
    ):
        self.start = start
        self.to = to
        self.pawn = pawn
        self.captured = captured.copy()

    def __str__(self):
        return f"Capture {self.pawn} {self.start} -> {self.to} captured: {[captured for captured in self.captured]}"

    def __repr__(self):
        return f"Capture {self.pawn} {self.start} -> {self.to} captured: {[captured for captured in self.captured]}"


class Forward(Move):
    def __init__(self, start: Tuple[int, int], to: Tuple[int, int], pawn: Pawn):
        self.start = start
        self.to = to
        self.pawn = pawn

    def __str__(self):
        return f"Forward {self.pawn} {self.start} -> {self.to}"

    def __repr__(self):
        return f"Forward {self.pawn} {self.start} -> {self.to}"
