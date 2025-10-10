"""Game orchestration for Tic-Tac-Toe with top-down design."""

from __future__ import annotations

from typing import Optional

from board import Board
from player import Player, HumanPlayer, ComputerPlayer


class Game:
    """Coordinates the game: routing turns, printing, and detecting the end state."""

    def __init__(self) -> None:
        self.board = Board()
        self.current: Optional[Player] = None
        self.other: Optional[Player] = None

    def choose_players(self) -> None:
        """
        Choose who is X and who is O.

        Options:
        1 - Human (X) vs Human (O)
        2 - Human (X) vs Computer (O)
        3 - Computer (X) vs Human (O)
        4 - Computer (X) vs Computer (O)
        """
        print("Choose matchup:")
        print("  1) Human (X) vs Human (O)")
        print("  2) Human (X) vs Computer (O)")
        print("  3) Computer (X) vs Human (O)")
        print("  4) Computer (X) vs Computer (O)")
        while True:
            choice = input("Select [1-4]: ").strip()
            if choice == "1":
                self.current, self.other = HumanPlayer("X"), HumanPlayer("O")
                return
            if choice == "2":
                self.current, self.other = HumanPlayer("X"), ComputerPlayer("O")
                return
            if choice == "3":
                self.current, self.other = ComputerPlayer("X"), HumanPlayer("O")
                return
            if choice == "4":
                self.current, self.other = ComputerPlayer("X"), ComputerPlayer("O")
                return
            print("Please enter 1, 2, 3 or 4.")

    def switch_player(self) -> None:
        """Swap the current and the other player."""
        self.current, self.other = self.other, self.current

    def play_one_turn(self) -> None:
        """Play a single turn."""
        assert self.current is not None
        move = self.current.choose_move(self.board)
        placed = self.board.place(move, self.current.symbol)
        if not placed:
            # Should not happen for computer; can happen for human due to race with input.
            print("Illegal move. Turn skipped.")
        self.board.render()

    def is_over(self) -> bool:
        """Return True when there is a winner or a draw."""
        return self.board.check_winner() is not None or self.board.is_full()

    def print_result(self) -> None:
        """Print the final outcome."""
        winner = self.board.check_winner()
        if winner:
            print(f"Player {winner} wins!")
        else:
            print("Draw.")

    def play(self) -> None:
        """Full game loop."""
        self.board.reset()
        self.board.render()
        self.choose_players()

        while not self.is_over():
            self.play_one_turn()
            if not self.is_over():
                self.switch_player()

        self.print_result()
