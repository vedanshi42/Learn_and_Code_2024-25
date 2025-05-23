import unittest
from main import DivisorCounter, DivisorPairMatcher


class TestDivisorCounter(unittest.TestCase):

    def test_divisors_of_1(self):
        self.assertEqual(DivisorCounter(1).count(), 1)

    def test_divisors_of_6(self):
        self.assertEqual(DivisorCounter(6).count(), 4)  # [1, 2, 3, 6]

    def test_divisors_of_prime(self):
        self.assertEqual(DivisorCounter(13).count(), 2)  # [1, 13]

    def test_divisors_of_perfect_square(self):
        self.assertEqual(DivisorCounter(16).count(), 5)  # [1, 2, 4, 8, 16]

    def test_zero_input(self):
        with self.assertRaises(ValueError):
            DivisorCounter(0)

    def test_negative_input(self):
        with self.assertRaises(ValueError):
            DivisorCounter(-10)


class TestDivisorPairMatcher(unittest.TestCase):

    def test_matching_pairs_n_4(self):
        self.assertEqual(DivisorPairMatcher(4).find_matching_pairs(), 1)

    def test_matching_pairs_n_1(self):
        self.assertEqual(DivisorPairMatcher(1).find_matching_pairs(), 0)

    def test_matching_pairs_even_n(self):
        self.assertEqual(DivisorPairMatcher(6).find_matching_pairs(), 1)

    def test_matching_pairs_odd_n(self):
        self.assertEqual(DivisorPairMatcher(5).find_matching_pairs(), 1)

    def test_matching_pairs_larger_n(self):
        self.assertEqual(DivisorPairMatcher(10).find_matching_pairs(), 1)

    def test_matching_pairs_large_input(self):
        self.assertEqual(DivisorPairMatcher(100).find_matching_pairs(), 15)

    def test_invalid_type_string(self):
        with self.assertRaises(TypeError):
            DivisorPairMatcher("10")

    def test_invalid_type_float(self):
        with self.assertRaises(TypeError):
            DivisorPairMatcher(5.5)

    def test_negative_input(self):
        with self.assertRaises(ValueError):
            DivisorPairMatcher(-4)

    def test_zero_input(self):
        with self.assertRaises(ValueError):
            DivisorPairMatcher(0)


if __name__ == "__main__":
    unittest.main()
