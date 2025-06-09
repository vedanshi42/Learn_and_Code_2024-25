from program_logic.divisor_pair_matcher import DivisorPairMatcher


class ProgramLogicExecutor:
    def __init__(self, number_of_test_cases: int):
        if number_of_test_cases <= 0:
            raise ValueError("Number of test cases must be positive integer.")
        self.number_of_test_cases = number_of_test_cases

    def run_test_cases(self) -> None:
        for test_case_num in range(1, self.number_of_test_cases + 1):
            print(f"\nTest Case {test_case_num}:")
            try:
                upper_limit = self.get_upper_limit()
                result = self.process_test_case(upper_limit)
                self.display_result(upper_limit, result)
            except ValueError as e:
                print(f"Error in Test Case {test_case_num}: {e}")
            except Exception as e:
                print(f"Unexpected error in Test Case {test_case_num}: {e}")

    def get_upper_limit(self) -> int:
        value = input("Enter the upper limit: ").strip()
        if not value:
            raise ValueError("Upper limit is required.")
        upper_limit = int(value)
        if upper_limit <= 0:
            raise ValueError("Upper limit must be a positive integer.")
        return upper_limit

    def process_test_case(self, upper_limit: int) -> int:
        matcher = DivisorPairMatcher(upper_limit)
        return matcher.find_matching_pairs()

    def display_result(self, upper_limit: int, result: int) -> None:
        print(f"Number of matching divisor pairs for {upper_limit}: {result}")
