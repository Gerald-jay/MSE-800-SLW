import unittest

# functions to test
def add(x, y):
    # Return the sum of two numbers.
    return x + y

def mul(x, y):
    # Return the product of two numbers.
    return x * y


# unit tests
class TestMathOperations(unittest.TestCase):
    #Unit tests for add() and mul() functions.

    def test_add(self):
        # Test addition function.
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)

    def test_mul(self):
        # Test multiplication function.
        self.assertEqual(mul(2, 3), 6)
        self.assertEqual(mul(-1, 5), -5)
        self.assertEqual(mul(0, 10), 0)
        self.assertEqual(mul(-2, -4), 8)


if __name__ == '__main__':
    unittest.main()
