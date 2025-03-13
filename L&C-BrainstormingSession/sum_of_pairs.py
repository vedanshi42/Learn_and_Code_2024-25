list_of_numbers_to_find_pairs = list(int(x) for x in input('Enter comma seperated list of numbers').split(','))
temp_list = list_of_numbers_to_find_pairs.copy()
result_pairs = []

for num in list_of_numbers_to_find_pairs:
    for other_num in list_of_numbers_to_find_pairs:
        if num + other_num == 10:
            pair_of_elements = (num, other_num)

            if num in temp_list and other_num in temp_list:
                result_pairs.append(pair_of_elements)
                temp_list.remove(num)
                temp_list.remove(other_num)

print(result_pairs)
