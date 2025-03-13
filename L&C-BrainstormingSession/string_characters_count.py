first_string = input('Enter first String: ')
second_string = input('Enter second String: ')

result_first_string = {}
result_second_string = {}

for char in first_string:
    if char in result_first_string:
        result_first_string[char] += 1
    else:
        result_first_string[char] = 1

for char in second_string:
    if char in result_second_string:
        result_second_string[char] += 1
    else:
        result_second_string[char] = 1

# Removing characters that appear more than once
repeated_first_string = {char: count for char, count in result_first_string.items() if count > 1}
repeated_second_string = {char: count for char, count in result_second_string.items() if count > 1}

print(f'Repeated characters in string 1: {repeated_first_string}')
print(f'Repeated characters in string 2: {repeated_second_string}')
