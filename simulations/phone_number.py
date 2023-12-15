
min_phone_number = 0
max_phone_number = 999_999_9999
check_str = "42"

check_number_count = 0

to_fill = len(str(max_phone_number))

for number in range(min_phone_number, max_phone_number+1):
    check_number_count += check_str in str(number).zfill(to_fill)

total_possible_numbers = max_phone_number - min_phone_number
print(f"{check_number_count} numbers have a {check_str}. That's {check_number_count / total_possible_numbers:%} of all numbers")