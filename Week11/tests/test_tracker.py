# Unit tests for the Personal Expense Tracker.

import unittest
from tracker import Expense, ExpenseTracker


class TestExpense(unittest.TestCase):
    # Tests for the Expense value object.

    def test_valid_expense(self):
        exp = Expense("Lunch", 12.5)
        self.assertEqual(exp.description, "Lunch")
        self.assertEqual(exp.amount, 12.5)

    def test_description_must_not_be_empty(self):
        with self.assertRaises(ValueError):
            Expense("", 1.0)
        with self.assertRaises(ValueError):
            Expense("   ", 1.0)

    def test_amount_non_negative_and_numeric(self):
        with self.assertRaises(ValueError):
            Expense("Taxi", -1)
        with self.assertRaises(TypeError):
            Expense("Taxi", "12")  # type: ignore[arg-type]


class TestExpenseTracker(unittest.TestCase):
    # Tests for the ExpenseTracker aggregate.

    def setUp(self):
        self.tracker = ExpenseTracker()

    def test_add_expense_returns_expense_and_is_listed(self):
        exp = self.tracker.add_expense("Coffee", 4.5)
        self.assertIsInstance(exp, Expense)
        self.assertIn(exp, self.tracker.list_expenses())

    def test_total_accumulates(self):
        self.tracker.add_expense("Coffee", 4.5)
        self.tracker.add_expense("Bus", 3.2)
        self.assertEqual(self.tracker.total(), 7.7)

    def test_seed_items_starting_state(self):
        seeded = ExpenseTracker(seed=[Expense("A", 1.0), Expense("B", 2.0)])
        self.assertEqual(seeded.total(), 3.0)
        self.assertEqual(len(seeded.list_expenses()), 2)


if __name__ == "__main__":
    unittest.main()