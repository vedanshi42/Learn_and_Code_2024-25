from program_logic.divisor_counter import DivisorCounter


class DivisorPairMatcher:
    def __init__(self, upper_limit: int):
        if not isinstance(upper_limit, int):
            raise TypeError("Input must be an integer.")
        if upper_limit <= 0:
            raise ValueError("Input must be a positive integer.")
        self.upper_limit = upper_limit

    def find_matching_pairs(self) -> int:
        count = 0
        for i in range(1, self.upper_limit):
            if DivisorCounter(i).count() == DivisorCounter(i + 1).count():
                count += 1
        return count
