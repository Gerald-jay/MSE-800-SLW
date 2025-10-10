"""Player module: abstract base, human player, and computer (random) player."""

from __future__ import annotations

import random
from abc import ABC, abstractmethod

from board import Board, Move


class Player(ABC):
    """Abstract player base class."""

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    @abstractmethod
    def choose_move(self, board: Board) -> Move:
        """Return a legal move on the given board."""
        raise NotImplementedError


class HumanPlayer(Player):
    """Human player who chooses a move via keyboard input."""

    def choose_move(self, board: Board) -> Move:
        while True:
            raw = input(f"Player {self.symbol} - enter move as row,col (e.g. 1,2): ").strip()
            try:
                row_str, col_str = (p.strip() for p in raw.split(","))
                row, col = int(row_str), int(col_str)
                move = Move(row, col)
                if move in board.empty_squares():
                    return move
                print("Cell is occupied or out of range. Try again.")
            except Exception:
                print("Invalid input. Use the format row,col with values 0..2.")


class ComputerPlayer(Player):
    """Computer player that picks randomly from available cells."""

    def choose_move(self, board: Board) -> Move:
        empties = board.empty_squares()
        return random.choice(empties)
