"""Board module for a 3x3 Tic-Tac-Toe game."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Move:
    """A move on the board (row, col)."""
    row: int
    col: int


class Board:
    """Represents a 3×3 Tic-Tac-Toe board and its rules."""

    def __init__(self) -> None:
        self.grid: list[list[str]] = [[" " for _ in range(3)] for _ in range(3)]

    def reset(self) -> None:
        """Clear the board to its initial empty state."""
        for r in range(3):
            for c in range(3):
                self.grid[r][c] = " "

    def render(self) -> None:
        """Print the board to stdout."""
        print("\n  0   1   2")
        for r in range(3):
            print(f"{r} " + " | ".join(self.grid[r]))
            if r < 2:
                print("  ---------")

    def place(self, move: Move, symbol: str) -> bool:
        """
        Place a symbol on the board if the target cell is empty.

        Returns:
            True when placed successfully, otherwise False.
        """
        if 0 <= move.row < 3 and 0 <= move.col < 3 and self.grid[move.row][move.col] == " ":
            self.grid[move.row][move.col] = symbol
            return True
        return False

    def empty_squares(self) -> list[Move]:
        """Return a list of currently empty cells."""
        return [Move(r, c) for r in range(3) for c in range(3) if self.grid[r][c] == " "]

    def check_winner(self) -> str | None:
        """Return 'X' or 'O' if someone wins; otherwise None."""
        lines: list[list[str]] = []
        lines.extend(self.grid)  # rows
        lines.extend([[self.grid[r][c] for r in range(3)] for c in range(3)])  # cols
        lines.append([self.grid[i][i] for i in range(3)])  # diag
        lines.append([self.grid[i][2 - i] for i in range(3)])  # anti-diag

        for line in lines:
            if line[0] != " " and line.count(line[0]) == 3:
                return line[0]
        return None

    def is_full(self) -> bool:
        """Return True when no empty squares remain."""
        return not any(" " in row for row in self.grid)
