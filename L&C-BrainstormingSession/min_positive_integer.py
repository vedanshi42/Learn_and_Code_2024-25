list_of_numbers = list(int(x) for x in input('Enter comma seperated list of integers').split(','))

max_range_to_check = int(input('Enter a positive integer to set maximum range to check'))
min_positive_integer = None

for current_value in range(1, max_range_to_check):
    if current_value in list_of_numbers:
        continue
    elif current_value not in list_of_numbers:
        min_positive_integer = current_value
        break
    else:
        print('No positive integer found in specified range which is not in input array')

print(f'the minimum positive integer not in this array is {min_positive_integer}')
