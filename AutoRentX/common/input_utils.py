# input_utils.py
# -*- coding: utf-8 -*-
"""
Common input helpers
Feature: default accepts Any (compatible with Peewee field descriptors), internally converted to basic types.
"""

from typing import Any, Optional
import re
from datetime import datetime

# ---------- Utility: Coerce Any to Built-in Types ----------
def _coerce_int(value: Any) -> int:
    if value is None:
        raise ValueError("default is None")
    # Peewee model attributes can usually be directly int(); fallback to str()
    try:
        return int(value)
    except Exception:
        return int(str(value))

def _coerce_float(value: Any) -> float:
    if value is None:
        raise ValueError("default is None")
    try:
        return float(value)
    except Exception:
        return float(str(value))

def _coerce_str(value: Any) -> str:
    if value is None:
        raise ValueError("default is None")
    return str(value)

# ---------- Input Functions ----------
def prompt_int(label: str, default: Any = None) -> int:
    """Integer input; default accepts Any and is internally converted to int."""
    while True:
        if default is not None:
            try:
                d = _coerce_int(default)
            except Exception:
                d = None
            s = input(f"{label} [{'' if d is None else d}]: ").strip()
            if s == "":
                if d is None:
                    print("✗ No usable default, please enter an integer")
                else:
                    return d
        else:
            s = input(f"{label}: ").strip()

        try:
            return int(s)
        except ValueError:
            print("✗ Please enter an integer")

def prompt_float(label: str, default: Any = None) -> float:
    """Float input; default accepts Any and is internally converted to float."""
    while True:
        if default is not None:
            try:
                d = _coerce_float(default)
            except Exception:
                d = None
            s = input(f"{label} [{'' if d is None else d}]: ").strip()
            if s == "":
                if d is None:
                    print("✗ No usable default, please enter a number")
                else:
                    return d
        else:
            s = input(f"{label}: ").strip()

        try:
            return float(s)
        except ValueError:
            print("✗ Please enter a number")

def prompt_str(label: str, default: Any = None) -> str:
    """String input; default accepts Any and is internally converted to str."""
    if default is not None:
        d = _coerce_str(default)
        s = input(f"{label} [{d}]: ").strip()
        return s if s else d
    else:
        return input(f"{label}: ").strip()

def prompt_choice(label: str, choices: list[str], default: Any = None) -> str:
    """Enum choice; default accepts Any and is internally converted to lowercase str."""
    choices_str = "/".join(choices)
    d = None
    if default is not None:
        d = _coerce_str(default).lower()
    while True:
        if d is not None:
            s = input(f"{label} ({choices_str}) [{d}]: ").strip().lower()
            if s == "":
                return d
        else:
            s = input(f"{label} ({choices_str}): ").strip().lower()

        if s in choices:
            return s
        print(f"✗ Allowed: {choices_str}")

def prompt_id(label: str = "ID") -> Optional[int]:
    """ID input, safely convert to int; return None if invalid."""
    s = input(f"{label}: ").strip()
    try:
        return int(s)
    except ValueError:
        print("✗ Please enter a numeric ID")
        return None

def prompt_date(label: str, default: Any = None, fmt: str = "%d-%m-%Y") -> str:
    """Date input (dd-mm-yyyy); default accepts Any (will be converted to str and parsed)."""
    d_str: Optional[str] = None
    if default is not None:
        d_str = _coerce_str(default)
        # If default is a datetime/date string, normalize it according to fmt
        try:
            d_dt = datetime.strptime(d_str, fmt)
            d_str = d_dt.strftime(fmt)
        except Exception:
            # If not matching fmt, prompt format when asking user to re-enter
            pass
            
    while True:
        if d_str is not None:
            s = input(f"{label} (format {fmt}) [{d_str}]: ").strip()
            if s == "":
                return d_str
        else:
            s = input(f"{label} (format {fmt}): ").strip()
        try:
            dt = datetime.strptime(s, fmt)
            return dt.strftime(fmt)
        except ValueError:
            print(f"✗ Invalid date format, expected {fmt}")

def prompt_date_range(
    label_start: str = "Start date",
    label_end: str = "End date",
    fmt: str = "%d-%m-%Y"
) -> tuple[str, str]:
    """Date range input (dd-mm-yyyy), validate end >= start."""
    while True:
        start = prompt_date(label_start, fmt=fmt)
        end = prompt_date(label_end, fmt=fmt)
        try:
            sdt = datetime.strptime(start, fmt)
            edt = datetime.strptime(end, fmt)
            if edt < sdt:
                print("✗ End date cannot be earlier than start date")
            else:
                return start, end
        except ValueError:
            print(f"✗ Invalid date format, expected {fmt}")

def prompt_email(label: str = "Email", default: Any = None) -> str:
    """Email input; default accepts Any and is internally converted to lowercase str and validated."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    d: Optional[str] = None
    if default is not None:
        d = _coerce_str(default).lower()
    while True:
        if d is not None:
            s = input(f"{label} [{d}]: ").strip().lower()
            if s == "":
                return d
        else:
            s = input(f"{label}: ").strip().lower()

        if re.match(pattern, s):
            return s
        print("✗ Invalid email format")
