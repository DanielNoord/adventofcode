# Solution to AoC 2020 day 2
import re

# Load password file
PASSWORDS = []
file = open("input.txt", "r")
for line in file:
    PASSWORDS.append(line.replace("\n", ""))
file.close()

# Check each lines
OTHER_CORRECT_COUNT = 0
TOBOGGAN_CORRECT_COUNT = 0
for line in PASSWORDS:
    groups = re.split(" ", line)
    limits = groups[0].split("-")
    letter = groups[1][0]
    if groups[2].count(letter) >= int(limits[0]) and groups[2].count(letter) <= int(limits[1]):
        OTHER_CORRECT_COUNT += 1
    if bool(groups[2][int(limits[0]) - 1] == letter) ^ bool(groups[2][int(limits[1]) - 1] == letter):
        TOBOGGAN_CORRECT_COUNT += 1
print(f"The number of correct passwords following other policy is: {OTHER_CORRECT_COUNT}")
print(f"The number of correct passwords following Toboggan policy is: {TOBOGGAN_CORRECT_COUNT}")
