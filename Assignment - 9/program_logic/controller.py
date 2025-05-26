from program_logic.program_logic_executor import ProgramLogicExecutor


class DivisorController:
    @staticmethod
    def main() -> None:
        try:
            number_of_test_cases = int(input("Enter the number of test cases: "))
            executor = ProgramLogicExecutor(number_of_test_cases)
            executor.execute()
        except ValueError as ve:
            print(f"Invalid input: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")
