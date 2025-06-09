import unittest
from program_logic.divisor_counter import DivisorCounter


class TestDivisorCounter(unittest.TestCase):

    def test_divisors_of_1(self):
        self.assertEqual(DivisorCounter(1).count(), 1)

    def test_divisors_of_6(self):
        self.assertEqual(DivisorCounter(6).count(), 4)

    def test_divisors_of_prime(self):
        self.assertEqual(DivisorCounter(13).count(), 2)

    def test_divisors_of_perfect_square(self):
        self.assertEqual(DivisorCounter(16).count(), 5)

    def test_zero_input(self):
        with self.assertRaises(ValueError):
            DivisorCounter(0)

    def test_negative_input(self):
        with self.assertRaises(ValueError):
            DivisorCounter(-10)
