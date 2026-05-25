from enum import Enum
from typing import Tuple, List


class PawnType(Enum):
    Pawn = 0
    Knight = 1


class PawnColor(Enum):
    Black = 0
    White = 1

    def opposite(self) -> "PawnColor":
        if self == PawnColor.White:
            return PawnColor.Black
        return PawnColor.White


class Pawn:
    x: int
    y: int
    type: PawnType
    color: PawnColor

    def __init__(self, x, y, color: PawnColor):
        self.type = PawnType.Pawn

        self.x = x
        self.y = y
        self.color = color

    def get_position(self) -> Tuple[int, int]:
        return self.x, self.y

    def get_color(self) -> PawnColor:
        return self.color

    def neighborhood(self) -> List[Tuple[int, int]]:
        neighbors: List[Tuple[int, int]] = []

        if self.x > 0 and self.y < 7:
            neighbors.append((self.x - 1, self.y + 1))
        if self.x > 0 and self.y > 0:
            neighbors.append((self.x - 1, self.y - 1))
        if self.x < 7 and self.y > 0:
            neighbors.append((self.x + 1, self.y - 1))
        if self.x < 7 and self.y < 7:
            neighbors.append((self.x + 1, self.y + 1))
        return neighbors

    def __str__(self):
        return f"({self.type.name}, ({self.x}, {self.y}), {self.color.name})"

    def __repr__(self):
        return f"({self.type.name}, ({self.x}, {self.y}), {self.color.name})"
