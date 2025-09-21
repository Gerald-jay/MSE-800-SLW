# common/typing_utils.py
# -*- coding: utf-8 -*-
"""
Typing utilities
"""

from typing import Any

def safe_pk(obj: Any) -> int:
    """
    Safely get Peewee model primary key
    - If obj is None, return 0
    - If obj has no id attribute, return 0
    - If obj.id is int/str, convertible to int
    - In other cases, return 0
    """
    if obj is None:
        return 0
    if not hasattr(obj, "id"):
        return 0
    val = getattr(obj, "id")
    if isinstance(val, (int, str)):
        try:
            return int(val)
        except ValueError:
            return 0
    return 0
