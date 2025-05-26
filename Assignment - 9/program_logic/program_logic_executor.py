from program_logic.divisor_pair_matcher import DivisorPairMatcher


class ProgramLogicExecutor:
    def __init__(self, number_of_test_cases: int):
        if number_of_test_cases <= 0:
            raise ValueError("Number of test cases must be a positive integer.")
        self.number_of_test_cases = number_of_test_cases

    def execute(self) -> None:
        for idx in range(1, self.number_of_test_cases + 1):
            print(f"\nTest Case {idx}:")
            try:
                upper_limit = int(input("Enter the upper limit: "))
                matcher = DivisorPairMatcher(upper_limit)
                result = matcher.find_matching_pairs()
                print(f"Number of matching divisor pairs for {upper_limit}: {result}")
            except (ValueError, TypeError) as e:
                print(f"Invalid input: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
