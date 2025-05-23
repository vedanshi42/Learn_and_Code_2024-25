def count_divisors(number):
    if number <= 0:
        raise ValueError("Input must be a positive integer greater than zero.")

    divisor_count = 0
    for potential_divisor in range(1, number + 1):
        if number % potential_divisor == 0:
            divisor_count += 1
    return divisor_count


def find_matching_divisor_pairs(upper_limit):
    if not isinstance(upper_limit, int):
        raise TypeError("Input must be an integer.")
    if upper_limit <= 0:
        raise ValueError("Input must be a positive integer greater than zero.")

    matching_pairs_count = 0
    for i in range(1, upper_limit + 1):
        first_number = i
        if (i+1) < (upper_limit + 1):
            second_number = i+1
        else:
            break
        if count_divisors(first_number) == count_divisors(second_number):
            matching_pairs_count += 1
    return matching_pairs_count


def main():
    try:
        number_of_test_cases = int(input("Enter the number of test cases: "))
        if number_of_test_cases <= 0:
            raise ValueError("Number of test cases must be positive integer.")

        for _ in range(number_of_test_cases):
            try:
                upper_limit = int(input("Enter the upper limit for the current test case: "))
                result = find_matching_divisor_pairs(upper_limit)
                print(f"Number of matching divisor pairs for {upper_limit}: {result}")
            except ValueError as ve:
                print(f"Invalid input: {ve}")
            except TypeError as te:
                print(f"Error: {te}")
            except Exception as e:
                print(f"Unexpected error: {e}")
    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
