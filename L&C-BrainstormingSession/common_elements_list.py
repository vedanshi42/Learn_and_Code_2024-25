first_list = list(int(x) for x in input('Enter comma seperated list of number for first array').split(','))
second_list = list(int(x) for x in input('Enter comma seperated list of numbers for second array').split(','))
third_list = list(int(x) for x in input('Enter comma seperated list of numbers for third array').split(','))

print(f'First Array: {first_list}')
print(f'Second Array: {second_list}')
print(f'Third Array: {third_list}')

common_elements_list = []

length_of_array = len(first_list) # Assumption is each array has same length

for element in first_list:
    if element in second_list and element in third_list:
        if element not in common_elements_list:
            common_elements_list.append(element)
    else:
        continue

print(common_elements_list)
