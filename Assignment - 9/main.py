class DivisorCounter:
    def __init__(self, number):
        if number <= 0:
            raise ValueError("Input must be a positive integer")
        self.number = number

    def count(self):
        return sum(1 for i in range(1, self.number + 1)
                   if self.number % i == 0)


class DivisorPairMatcher:
    def __init__(self, upper_limit):
        if not isinstance(upper_limit, int):
            raise TypeError("Input must be an integer.")
        if upper_limit <= 0:
            raise ValueError("Input must be a positive integer")
        self.upper_limit = upper_limit

    def find_matching_pairs(self):
        count = 0
        for i in range(1, self.upper_limit):
            first_count = DivisorCounter(i).count()
            second_count = DivisorCounter(i + 1).count()
            if first_count == second_count:
                count += 1
        return count


class TestCaseRunner:
    def __init__(self, number_of_test_cases):
        if number_of_test_cases <= 0:
            raise ValueError("Number of test cases must be positive integer.")
        self.number_of_test_cases = number_of_test_cases

    def run(self):
        for idx in range(1, self.number_of_test_cases + 1):
            print(f"\nTest Case {idx}:")
            try:
                upper_limit = int(input("Enter the upper limit: "))
                matcher = DivisorPairMatcher(upper_limit)
                result = matcher.find_matching_pairs()
                print(f"Number of matching divisor pairs for {upper_limit}: {result}")
            except ValueError as ve:
                print(f"Invalid input: {ve}")
            except TypeError as te:
                print(f"Error: {te}")
            except Exception as e:
                print(f"Unexpected error: {e}")


class Application:
    @staticmethod
    def main():
        try:
            number_of_test_cases = int(input("Enter the number of test cases: "))
            runner = TestCaseRunner(number_of_test_cases)
            runner.run()
        except ValueError as ve:
            print(f"Invalid input: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    Application.main()
