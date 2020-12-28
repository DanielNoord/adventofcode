# Solution to AoC 2020 day 4

import re

# Load Map file
PASSPORTS = []
file = open("input.txt", "r")
PASSPORTS = file.read().split("\n\n")
CLEAN_PASSPORTS = []
for pp in PASSPORTS:
    passport_fields = dict(pair.split(':') for pair in pp.split())
    CLEAN_PASSPORTS.append(passport_fields)

REQUIRED_FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
VALID_PASSPORTS = 0
for passport in CLEAN_PASSPORTS:
    valid = 0
    missing_field = REQUIRED_FIELDS - passport.keys()
    if missing_field == set():
        valid += 1
    if passport.get('byr') and 1920 <= int(passport['byr']) <= 2002:
        valid += 1
    if passport.get('iyr') and 2010 <= int(passport['iyr']) <= 2020:
        valid += 1
    if passport.get('eyr') and 2020 <= int(passport['eyr']) <= 2030:
        valid += 1
    if passport.get('hcl') and re.compile(r'^#[\da-z]{6}$').match(passport['hcl']) is not None:
        valid += 1
    if passport.get('ecl') and passport['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
        valid += 1
        print(valid)
    if passport.get('pid') and re.compile(r'^\d{9}$').match(passport['pid']) is not None:
        valid += 1
    if passport.get('hgt'):
        height, unit = re.compile(r'^(\d+)(in|cm)?$').match(passport['hgt']).groups()
        if unit == 'cm' and 150 <= int(height) <= 193:
            valid += 1
        elif unit == 'in' and 59 <= int(height) <=  76:
            valid += 1
    if valid == 8:
        VALID_PASSPORTS += 1

print(VALID_PASSPORTS)