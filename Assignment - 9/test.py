import unittest
from main import count_divisors, find_matching_divisor_pairs


class TestDivisorFunctions(unittest.TestCase):

    def test_count_divisors_of_1(self):
        self.assertEqual(count_divisors(1), 1)

    def test_count_divisors_of_6(self):
        self.assertEqual(count_divisors(6), 4)  # Divisors: [1, 2, 3, 6]

    def test_count_divisors_of_prime(self):
        self.assertEqual(count_divisors(13), 2)  # Divisors: [1, 13]

    def test_count_divisors_of_perfect_square(self):
        self.assertEqual(count_divisors(16), 5)  # Divisors: [1, 2, 4, 8, 16]

    def test_count_divisors_of_zero(self):
        with self.assertRaises(ValueError):
            count_divisors(0)

    def test_count_divisors_of_negative(self):
        with self.assertRaises(ValueError):
            count_divisors(-10)

    # --- find_matching_divisor_pairs tests ---

    def test_matching_pairs_for_n_4(self):
        self.assertEqual(find_matching_divisor_pairs(4), 1)

    def test_matching_pairs_for_n_1(self):
        self.assertEqual(find_matching_divisor_pairs(1), 0)

    def test_matching_pairs_for_even_n(self):
        self.assertEqual(find_matching_divisor_pairs(6), 1)

    def test_matching_pairs_for_odd_n(self):
        self.assertEqual(find_matching_divisor_pairs(5), 1)

    def test_matching_pairs_for_larger_n(self):
        self.assertEqual(find_matching_divisor_pairs(10), 1)

    def test_matching_pairs_for_large_input(self):
        self.assertEqual(find_matching_divisor_pairs(100), 15)

    # --- Edge case and invalid input tests ---

    def test_invalid_type_for_matching_pairs(self):
        with self.assertRaises(TypeError):
            find_matching_divisor_pairs("10")

    def test_invalid_float_for_matching_pairs(self):
        with self.assertRaises(TypeError):
            find_matching_divisor_pairs(5.5)

    def test_negative_input_for_matching_pairs(self):
        with self.assertRaises(ValueError):
            find_matching_divisor_pairs(-4)

    def test_zero_input_for_matching_pairs(self):
        with self.assertRaises(ValueError):
            find_matching_divisor_pairs(0)


if __name__ == "__main__":
    unittest.main()
