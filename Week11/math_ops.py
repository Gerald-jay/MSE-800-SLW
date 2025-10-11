"""Basic math operations with doctests: +, -, /, %.

Quick doctest suite
===================

>>> add(2, 3)
5
>>> sub(10, 4)
6
>>> div(6, 3)
2.0
>>> mod(10, 3)
1

Type validation:

>>> add("2", 3)
Traceback (most recent call last):
...
TypeError: both x and y must be numbers

Division by zero:

>>> div(1, 0)
Traceback (most recent call last):
...
ZeroDivisionError: division by zero
"""

from __future__ import annotations
from typing import Union

Number = Union[int, float]


def _ensure_numbers(x: object, y: object) -> tuple[Number, Number]:
    """Return (x, y) as numbers or raise TypeError."""
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError("both x and y must be numbers")
    return x, y


def add(x: Number, y: Number) -> Number:
    """Return x + y.

    >>> add(1, 2)
    3
    """
    a, b = _ensure_numbers(x, y)
    return a + b


def sub(x: Number, y: Number) -> Number:
    """Return x - y.

    >>> sub(5, 2)
    3
    """
    a, b = _ensure_numbers(x, y)
    return a - b


def div(x: Number, y: Number) -> float:
    """Return x / y as float. Raises ZeroDivisionError if y == 0.

    >>> div(9, 3)
    3.0
    """
    a, b = _ensure_numbers(x, y)
    return a / b  # Python 会在 int/int 时返回 float / Python will return float for int/int


def mod(x: Number, y: Number) -> Number:
    """Return x % y. Raises ZeroDivisionError if y == 0.

    >>> mod(10, 3)
    1
    """
    a, b = _ensure_numbers(x, y)
    return a % b


if __name__ == "__main__":
    # can be run via `python -m doctest math_ops.py -v`
    import doctest
    doctest.testmod(verbose=True)
