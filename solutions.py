#! /usr/bin/env python3

import re
import time

INPUT_FILES = dict((f"day{i+1}", f"inputs/input{i+1}.txt") for i in range(25))

# https://adventofcode.com/2020/day/1
def day1(input_file):
    expenses = [int(i) for i in input_file.split()]
    # Find pair that sum to 2020
    for item in expenses:
        if remainder := 2020 - item in expenses:
            print(f"The product of the two items summing to 2020 is: {remainder * item}")
            continue
        # Find three items that sum to 2020
        for item2 in expenses[expenses.index(item) + 1:]:
            if remainder := 2020 - item - item2 in expenses:
                print(f"The product of the three items summing to 2020 is: {remainder * item * item2}")
                break
        else:
            continue
        break


# https://adventofcode.com/2020/day/2
def day2(input_file):
    passwords = input_file.split("\n")
    # Check each lines
    other_correct_count = 0
    toboggan_correct_count = 0
    for line in passwords:
        groups = re.split(" ", line)
        limits = groups[0].split("-")
        letter = groups[1][0]
        if groups[2].count(letter) >= int(limits[0]) and groups[2].count(letter) <= int(limits[1]):
            other_correct_count += 1
        if bool(groups[2][int(limits[0]) - 1] == letter) ^ bool(groups[2][int(limits[1]) - 1] == letter):
            toboggan_correct_count += 1
    print(f"The number of correct passwords following other policy is: {other_correct_count}")
    print(f"The number of correct passwords following Toboggan policy is: {toboggan_correct_count}")


# https://adventofcode.com/2020/day/3
def day3(input_file):
    input_map = input_file.split("\n")
    input_map_width = len(input_map[0])

    def check_trees(vertical, horizontal):
        pointer = [0, 0]
        trees = 0
        for _ in range(0, len(input_map) - 1, vertical):
            pointer[0] += vertical
            pointer[1] += horizontal
            if input_map[pointer[0]][pointer[1] % input_map_width] == "#":
                trees += 1
        print(f"With a slope of {horizontal} right and {vertical} down you will encounter {trees} trees")
        return trees

    check_trees(1, 3)
    print(f"Sum of all trees: {check_trees(1, 1) * check_trees(1, 3) * check_trees(1, 5) * check_trees(1, 7) * check_trees(2, 1)}")


# https://adventofcode.com/2020/day/4
def day4(input_file):
    # Load input_map file
    passports = input_file.split("\n\n")
    clean_passports = []
    for passp in passports:
        passport_fields = dict(pair.split(':') for pair in passp.split())
        clean_passports.append(passport_fields)

    required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    valid_passports = 0
    for passport in clean_passports:
        valid = 0
        missing_field = required_fields - passport.keys()
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
        if passport.get('pid') and re.compile(r'^\d{9}$').match(passport['pid']) is not None:
            valid += 1
        if passport.get('hgt'):
            height, unit = re.compile(r'^(\d+)(in|cm)?$').match(passport['hgt']).groups()
            if unit == 'cm' and 150 <= int(height) <= 193:
                valid += 1
            elif unit == 'in' and 59 <= int(height) <= 76:
                valid += 1
        if valid == 8:
            valid_passports += 1

    print(f"There are {valid_passports} valid passports")


# https://adventofcode.com/2020/day/5
def day5(input_file):
    taken_seats = input_file.split("\n")

    def find_row(row_id):
        left = 128
        row_nr = 0
        for i in row_id:
            if i == 'B':
                row_nr += left // 2
            left //= 2
        return row_nr


    def find_column(column_id):
        left = 8
        column_nr = 0
        for i in column_id:
            if i == 'R':
                column_nr += left // 2
            left //= 2
        return column_nr


    max_id = 0
    seat_ids = []
    for seat in taken_seats:
        row, column = find_row(seat[:7]), find_column(seat[7:])
        if (seat_id := row * 8 + column) > max_id:
            max_id = seat_id
        seat_ids.append(seat_id)
    seat_ids.sort()
    missing_id = 0

    for seat in seat_ids:
        if seat + 1 not in seat_ids:
            missing_id = seat + 1
            break

    print(f"The highest id is {max_id} and your seat id is {missing_id}")


# https://adventofcode.com/2020/day/6
def day6(input_file):
    groups = input_file.split("\n\n")
    num_questions = 0
    for group in groups:
        questions = {}
        group = group.split("\n")
        for individual in group:
            for answer in individual:
                if questions.get(answer):
                    questions[answer] += 1
                else:
                    questions[answer] = 1
        for question in questions:
            if questions[question] == len(group):
                num_questions += 1
    print(f"The sum of questions is {num_questions}")


# https://adventofcode.com/2020/day/7
def day7(input_file):
    def count_bags(bag):
        # Substract 1 from to total to not count initial bag
        ret = 1
        for bags in rules_dict[bag]:
            ret += int(bags[1]) * count_bags(bags[0])
        return ret

    def traverse_rules(bag):
        for bags in rules_dict[bag]:
            if bags[0] == 'shiny gold':
                return 1
            if traverse_rules(bags[0]):
                return 1
        return 0

    rules_dict = {}
    rules = input_file.split("\n")
    start_pattern = re.compile(r'(.*?) (?=bags contain)')
    content_pattern = re.compile(r'(\d) (.*?) (?=bags?[,.])')
    for rule in rules:
        rule_parts = content_pattern.findall(rule)
        bag_name = start_pattern.match(rule).groups()[0]
        rules_dict[bag_name] = []
        for sub_rule in rule_parts:
            rules_dict[bag_name].append((sub_rule[1], sub_rule[0]))

    number_of_valid_bags = 0
    for i in rules_dict:
        number_of_valid_bags += traverse_rules(i)

    print(f"The sum of valid bags is {number_of_valid_bags}")
    print(f"The sum of bags inside the shiny gold bag is " + str(count_bags("shiny gold") - 1))


# https://adventofcode.com/2020/day/8
def day8(input_file):
    original_instructions = [i.split(" ") + [False] for i in input_file.split("\n")]

    def run_instruction(instructions):
        accumulator = 0
        pointer = 0
        full_run = False
        while not instructions[pointer][2]:
            instructions[pointer][2] = True
            if instructions[pointer][0] == "acc":
                accumulator += int(instructions[pointer][1])
            elif instructions[pointer][0] == "jmp":
                pointer += int(instructions[pointer][1])
                continue
            elif instructions[pointer][0] == "nop":
                pass
            pointer += 1
            if pointer + 1 == len(instructions):
                full_run = True
                break
        return (str(accumulator), full_run)
    # Task 1
    print(f"The state of the accumulator before the infinite loop is " + run_instruction(original_instructions)[0])
    # Task 2
    for i in range(len(original_instructions)):
        copied_instructions = [i.split(" ") + [False] for i in input_file.split("\n")]
        if copied_instructions[i][0] == "jmp":
            copied_instructions[i][0] = "nop"
        elif copied_instructions[i][0] == "nop":
            copied_instructions[i][0] = "jmp"
        accumulator_value, run_completed = run_instruction(copied_instructions)
        if run_completed:
            print(f"The state of the accumulator before the faulty instruction is {accumulator_value}")
            break


def solver(day):
    start = time.time()
    with open(INPUT_FILES[day], "r") as file:
        globals()[day](file.read())
    print(f"Execution of solution for {day} took {round((time.time() - start) * 1000, 5)} ms")

def all_days():
    totaltime = time.time()
    for i in range(7):
        print(f"===== DAY {i+1:2d} =====")
        solver(f"day{i+1}")
        print()
    print(f"Execution of all solutions took {round((time.time() - totaltime) * 1000, 5)} ms")

solver("day8")
