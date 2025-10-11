
"""Personal Expense Tracker (OOP) with doctests.

Features:
- add_expense(description, amount)
- total() -> float
- list_expenses() -> tuple[Expense, ...]

Quick doctest demo
==================

Create a tracker and add two expenses:

>>> t = ExpenseTracker()
>>> _ = t.add_expense("Coffee", 4.5)
>>> _ = t.add_expense("Bus", 3.2)
>>> t.total()
7.7

Validation errors:

>>> Expense("", 1.0)
Traceback (most recent call last):
...
ValueError: description must be non-empty

>>> Expense("Taxi", -1)
Traceback (most recent call last):
...
ValueError: amount must be >= 0

>>> Expense("Taxi", "12")  # type: ignore[arg-type]
Traceback (most recent call last):
...
TypeError: amount must be a number
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Expense:
    """Immutable value object representing a single expense item.

    Args:
        description: A non-empty description.
        amount: Non-negative numeric amount.

    Example (doctest):

    >>> Expense("Lunch", 12.5)
    Expense(description='Lunch', amount=12.5)
    """
    description: str
    amount: float

    def __post_init__(self) -> None:
        if not self.description or not self.description.strip():
            raise ValueError("description must be non-empty")
        if not isinstance(self.amount, (int, float)):
            raise TypeError("amount must be a number")
        if self.amount < 0:
            raise ValueError("amount must be >= 0")


class ExpenseTracker:
    """Tracks and manages multiple expenses.

    Example (doctest):

    >>> tracker = ExpenseTracker()
    >>> tracker.add_expense("Tea", 3.0)
    Expense(description='Tea', amount=3.0)
    >>> tracker.add_expense("Snacks", 2.25)
    Expense(description='Snacks', amount=2.25)
    >>> tracker.total()
    5.25
    >>> [e.description for e in tracker.list_expenses()]
    ['Tea', 'Snacks']
    """

    def __init__(self, seed: Iterable[Expense] | None = None) -> None:
        self._items: list[Expense] = list(seed or ())

    def add_expense(self, description: str, amount: float) -> Expense:
        """Create and store an expense; returns the created Expense.

        Example (doctest):

        >>> tr = ExpenseTracker()
        >>> tr.add_expense("Book", 10.0)
        Expense(description='Book', amount=10.0)
        """
        exp = Expense(description=description, amount=float(amount))
        self._items.append(exp)
        return exp

    def total(self) -> float:
        """Return the sum of all expense amounts (rounded to 2 decimals).

        Example (doctest):

        >>> tr = ExpenseTracker([Expense("A", 1), Expense("B", 2.555)])
        >>> tr.total()
        3.56
        """
        return round(sum(e.amount for e in self._items), 2)

    def list_expenses(self) -> tuple[Expense, ...]:
        """Return an immutable snapshot of expenses.

        Example (doctest):

        >>> tr = ExpenseTracker([Expense("A", 1), Expense("B", 2)])
        >>> tr.list_expenses()
        (Expense(description='A', amount=1), Expense(description='B', amount=2))
        """
        return tuple(self._items)


if __name__ == "__main__":
    # Tiny demo (optional)
    tracker = ExpenseTracker()
    tracker.add_expense("Coffee", 4.5)
    tracker.add_expense("Bus", 3.2)
    print("Total:", tracker.total())
