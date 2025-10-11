"""Unittests for math_ops: add, sub, div, mod."""

import unittest
import math
from math_ops import add, sub, div, mod


class TestAdd(unittest.TestCase):
    """Tests for add()."""

    def test_add_basic(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)

    def test_add_type_validation(self):
        with self.assertRaises(TypeError):
            add("2", 3)  # type: ignore[arg-type]


class TestSub(unittest.TestCase):
    """Tests for sub()."""

    def test_sub_basic(self):
        self.assertEqual(sub(10, 4), 6)
        self.assertEqual(sub(-1, -1), 0)


class TestDiv(unittest.TestCase):
    """Tests for div()."""

    def test_div_basic(self):
        self.assertEqual(div(6, 3), 2.0)
        self.assertTrue(math.isclose(div(7, 2), 3.5))

    def test_div_zero(self):
        with self.assertRaises(ZeroDivisionError):
            div(1, 0)

    def test_div_type_validation(self):
        with self.assertRaises(TypeError):
            div("6", 3)  # type: ignore[arg-type]


class TestMod(unittest.TestCase):
    """Tests for mod()."""

    def test_mod_basic(self):
        self.assertEqual(mod(10, 3), 1)
        self.assertEqual(mod(9, 3), 0)

    def test_mod_zero_divisor(self):
        with self.assertRaises(ZeroDivisionError):
            mod(1, 0)

    def test_mod_type_validation(self):
        with self.assertRaises(TypeError):
            mod(10, "3")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main(verbosity=2)