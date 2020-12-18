# Solution to AoC 2020 day 1

# Load expenses file
EXPENSES = []
file = open("input.txt", "r")
for line in file:
    EXPENSES.append(int(line.replace("\n", "")))
file.close()

# Find pair that sum to 2020
for item in EXPENSES:
    if (remainder := 2020 - item) in EXPENSES:
        print(f"The product of the two items summing to 2020 is: {remainder * item}")
        continue
    # Find three items that sum to 2020
    for item2 in EXPENSES[EXPENSES.index(item) + 1:]:
        if (remainder := 2020 - item - item2) in EXPENSES:
            print(f"The product of the three items summing to 2020 is: {remainder * item * item2}")
            break
    else:
        continue
    break
