def find_index(array, value):
    for index in range(len(array)):
        if array[index] == value:
            return index


def calculate_mean(array, lower_limit, upper_limit):
    lower_limit_index = find_index(array, lower_limit)
    upper_limit_index = find_index(array, upper_limit)

    if lower_limit_index > upper_limit_index:
        lower_limit_index, upper_limit_index = upper_limit_index, lower_limit_index

    subarray_sum = sum(array[lower_limit_index: upper_limit_index + 1])
    subarray_length = upper_limit_index - lower_limit_index + 1
    return subarray_sum // subarray_length


def process_queries(array, queries):
    for lower_limit, upper_limit in queries:
        print(f"expected value for query ({lower_limit, upper_limit}) is {calculate_mean(array, lower_limit, upper_limit)}")


def main():
    number_of_elements = int(input('Enter number of array elements: '))
    array = list(int(x) for x in input("Enter comma seperated array elements: ").split(','))
    number_of_queries = int(input('Enter number of queries: '))

    queries = [tuple(map(int, input('Enter query: ').split(','))) for _ in range(number_of_queries)]

    process_queries(array, queries)


main()
