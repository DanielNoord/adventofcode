#! /usr/bin/env python3
import operator
import re
import time
from collections import deque

INPUT_FILES = dict((f"day{i+1}", f"inputs/input{i+1}.txt") for i in range(25))

# https://adventofcode.com/2020/day/1
def day1(input_file):
    expenses = [int(i) for i in input_file.split()]

    complements = set()
    for item in expenses:
        if item in complements:
            print(f"The product of two items summing to 2020 is: {(2020 - item) * item}")
            break
        complements.add(2020 - item)

    for i, item in enumerate(expenses):
        compls = set()
        remainder = 2020 - item

        for item2 in expenses[i + 1 :]:
            item3 = remainder - item2
            if item2 in compls:
                print(f"The product of three items summing to 2020 is: {item * item2 * item3}")
                break
            compls.add(item3)


# https://adventofcode.com/2020/day/2
def day2(input_file):
    passwords = input_file.split("\n")
    other_correct_count = 0
    toboggan_correct_count = 0
    for line in passwords:
        groups = re.split(" ", line)
        limits = groups[0].split("-")
        letter = groups[1][0]
        if groups[2].count(letter) >= int(limits[0]) and groups[2].count(letter) <= int(limits[1]):
            other_correct_count += 1
        if bool(groups[2][int(limits[0]) - 1] == letter) ^ bool(
            groups[2][int(limits[1]) - 1] == letter
        ):
            toboggan_correct_count += 1
    print(f"The number of correct passwords following other policy is: {other_correct_count}")
    print(f"The number of correct passwords following Toboggan policy is: {toboggan_correct_count}")


# https://adventofcode.com/2020/day/3
def day3(input_file):
    input_map = input_file.split("\n")
    input_map_width = len(input_map[0])

    def trees(vertical, horizontal):
        pointer = [0, 0]
        trees = 0
        for _ in range(0, len(input_map) - 1, vertical):
            pointer[0] += vertical
            pointer[1] += horizontal
            if input_map[pointer[0]][pointer[1] % input_map_width] == "#":
                trees += 1
        print(f"With a slope of {horizontal} right and {vertical} down you encounter {trees} trees")
        return trees

    trees(1, 3)
    print(
        "Sum of all trees: ",
        trees(1, 1) * trees(1, 3) * trees(1, 5) * trees(1, 7) * trees(2, 1),
    )


# https://adventofcode.com/2020/day/4
def day4(input_file):
    # Load input_map file
    passports = input_file.split("\n\n")
    clean_passports = []
    for passp in passports:
        passport_fields = dict(pair.split(":") for pair in passp.split())
        clean_passports.append(passport_fields)

    required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    valid_passports = 0
    for passp in clean_passports:
        valid = 0
        missing_field = required_fields - passp.keys()
        if missing_field == set():
            valid += 1
        if passp.get("byr") and 1920 <= int(passp["byr"]) <= 2002:
            valid += 1
        if passp.get("iyr") and 2010 <= int(passp["iyr"]) <= 2020:
            valid += 1
        if passp.get("eyr") and 2020 <= int(passp["eyr"]) <= 2030:
            valid += 1
        if passp.get("hcl") and re.compile(r"^#[\da-z]{6}$").match(passp["hcl"]) is not None:
            valid += 1
        if passp.get("ecl") and passp["ecl"] in {
            "amb",
            "blu",
            "brn",
            "gry",
            "grn",
            "hzl",
            "oth",
        }:
            valid += 1
        if passp.get("pid") and re.compile(r"^\d{9}$").match(passp["pid"]) is not None:
            valid += 1
        if passp.get("hgt"):
            height, unit = re.compile(r"^(\d+)(in|cm)?$").match(passp["hgt"]).groups()
            if unit == "cm" and 150 <= int(height) <= 193:
                valid += 1
            elif unit == "in" and 59 <= int(height) <= 76:
                valid += 1
        valid_passports += valid // 8

    print(f"There are {valid_passports} valid passports")


# https://adventofcode.com/2020/day/5
def day5(input_file):
    taken_seats = input_file.split("\n")

    def find_row(row_id):
        left = 128
        row_nr = 0
        for i in row_id:
            if i == "B":
                row_nr += left // 2
            left //= 2
        return row_nr

    def find_column(column_id):
        left = 8
        column_nr = 0
        for i in column_id:
            if i == "R":
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
            if bags[0] == "shiny gold":
                return 1
            if traverse_rules(bags[0]):
                return 1
        return 0

    rules_dict = {}
    rules = input_file.split("\n")
    start_pattern = re.compile(r"(.*?) (?=bags contain)")
    content_pattern = re.compile(r"(\d) (.*?) (?=bags?[,.])")
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
    print(f"The sum of bags inside the shiny gold bag is {count_bags('shiny gold') - 1}")


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
    print(
        "The accumulator before infinite loop is at ",
        run_instruction(original_instructions)[0],
    )
    # Task 2
    for i in range(len(original_instructions)):
        copied_instructions = [i.split(" ") + [False] for i in input_file.split("\n")]
        if copied_instructions[i][0] == "jmp":
            copied_instructions[i][0] = "nop"
        elif copied_instructions[i][0] == "nop":
            copied_instructions[i][0] = "jmp"
        accumulator_value, run_completed = run_instruction(copied_instructions)
        if run_completed:
            print(
                "The accumulator before faulty instruction loop is at ",
                accumulator_value,
            )
            break


# https://adventofcode.com/2020/day/9
def day9(input_file):
    number_input = [int(i) for i in input_file.split("\n")]
    preamble = []

    def find_xmas_number(numbers):
        for number in numbers:
            preamble.append(number)
            if len(preamble) > 25:
                i = 0
                while i < 25:
                    if number - preamble[i] in preamble[:25]:
                        break
                    i += 1
                else:
                    return number
                preamble.pop(0)

    def find_weakness(data, target):
        for i in enumerate(data):
            current_sum = [0]
            j = i[0]
            while current_sum[0] < target:
                current_sum[0] += data[j]
                current_sum.append(data[j])
                if current_sum[0] == int(target):
                    return max(current_sum[1:]) + min(current_sum[1:])
                j += 1

    solution_task1 = find_xmas_number(number_input)
    print(f"The first incorrect number is {solution_task1}")
    print(f"The encryption weakness is {find_weakness(number_input, solution_task1)}")


# https://adventofcode.com/2020/day/10
def day10(input_file):
    adapters = [0] + sorted([int(i) for i in input_file.split()])
    jumps = [0, 0, 1]
    for i in enumerate(adapters[:-1]):
        jumps[adapters[i[0] + 1] - i[1] - 1] += 1

    # Based on solutions.py from https://github.com/warbaque/adventofcode-2020
    def find_paths():
        counter = deque([(0, 1)], maxlen=3)
        for adapter in adapters[1:]:
            ways = sum(w for j, w in counter if adapter - j <= 3)
            counter.append((adapter, ways))
        return counter[2][1]

    print(f"The multiple of 1 and 3 step adapters is {jumps[0] * jumps[2]}")
    print(f"The number of arrangements is {find_paths()}")


# https://adventofcode.com/2020/day/11
# Runs much faster with pypy, but need to remove f-strings
def day11(input_file):
    grid = input_file.split()

    height = len(grid)
    width = len(grid[0])

    def neighbour(grid_to_check, xcoord, ycoord, i, j):
        if (0 <= xcoord + i < width) and (0 <= ycoord + j < height) and (i != 0 or j != 0):
            return grid_to_check[ycoord + j][xcoord + i] == "#"
        return False

    def visible(grid_to_check, xcoord, ycoord, i, j):
        while True:
            xcoord += i
            ycoord += j
            if not ((0 <= xcoord < width) and (0 <= ycoord < height) and (i != 0 or j != 0)):
                break
            if grid_to_check[ycoord][xcoord] == ".":
                continue
            return grid_to_check[ycoord][xcoord] == "#"
        return False

    def do_round(old_grid, check, max_neighbours):
        new_grid = ["" for i in range(height)]
        occupied_seats = 0
        for line in enumerate(old_grid):
            for place in enumerate(line[1]):
                if place[1] == ".":
                    new_grid[line[0]] += "."
                    continue
                neighbours = 0
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        neighbours += check(old_grid, place[0], line[0], i, j)
                if place[1] == "L":
                    if neighbours == 0:
                        new_grid[line[0]] += "#"
                        occupied_seats += 1
                    else:
                        new_grid[line[0]] += "L"
                elif place[1] == "#":
                    if neighbours >= max_neighbours:
                        new_grid[line[0]] += "L"
                    else:
                        new_grid[line[0]] += "#"
                        occupied_seats += 1
        return new_grid, occupied_seats

    def run(grid, check, max_neighbours):
        previous_grid = []
        while previous_grid != grid:
            previous_grid = grid
            grid, number_of_occupied = do_round(previous_grid, check, max_neighbours)
        return number_of_occupied

    print(f"Number of occupied seats after no changes is {run(grid, neighbour, 4)}")
    print(f"Number of occupied seats after no changes with second rule is {run(grid, visible, 5)}")


# https://adventofcode.com/2020/day/12
def day12(input_file):
    directs = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}
    heads = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    instructions = [(i[0], int(i[1:])) for i in input_file.split()]
    pos = (0, 0)
    head = 1

    for direct, val in instructions:
        if direct == "F":
            pos = tuple(x + y for x, y in zip(pos, (val * heads[head][0], val * heads[head][1])))
        elif direct == "R":
            head = (head + val // 90) % 4
        elif direct == "L":
            head = ((head - val // 90) + 4) % 4
        else:
            pos = tuple(x + y for x, y in zip(pos, tuple(val * i for i in directs[direct])))
    print(f"The Manhattan Distance after instruction is {abs(pos[0]) + abs(pos[1])}")

    pos = (0, 0)
    wayp = (10, 1)
    for direct, val in instructions:
        if direct == "F":
            pos = tuple(x + y for x, y in zip(pos, (val * wayp[0], val * wayp[1])))
        elif direct == "R":
            for _ in range(val // 90):
                wayp = (wayp[1], -wayp[0])
        elif direct == "L":
            for _ in range(val // 90):
                wayp = (-wayp[1], wayp[0])
        else:
            wayp = tuple(x + y for x, y in zip(wayp, tuple(val * i for i in directs[direct])))
    print(f"The Manhattan Distance after second instruction is {abs(pos[0]) + abs(pos[1])}")


# https://adventofcode.com/2020/day/13
def day13(input_file):
    arrival, busses = input_file.split()
    busses = busses.split(",")
    busses = [(int(i), busses.index(i)) for i in busses if i != "x"]

    times = {}
    for bus in busses:
        times[bus[0] - (int(arrival) % bus[0])] = bus[0]
    min_minutes = min(times.keys())
    print(
        "Earliest possible bus ID times minutes waiting is ",
        times[min_minutes] * min_minutes,
    )

    timestamp = (0, busses[0][0])

    def find_time(base_time, next_bus):
        new_time = base_time[0]
        while True:
            new_time += base_time[1]
            if (new_time + next_bus[1]) % next_bus[0] == 0:
                return (new_time, base_time[1] * next_bus[0])

    for bus in enumerate(busses[:-1]):
        timestamp = find_time(timestamp, busses[bus[0] + 1])
    print("The earliest timestamp is ", timestamp[0])


# https://adventofcode.com/2020/day/14
def day14(input_file):
    code = input_file.split("\n")

    def write_memory(adress, val, offset, mem):
        if offset == 36:
            mem[int(adress, 2)] = val
            return
        for bit in enumerate(adress[offset:]):
            bit = (bit[0] + offset, bit[1])
            if bit[1] == "X":
                write_memory(adress[: bit[0]] + "0" + adress[bit[0] + 1 :], val, bit[0] + 1, mem)
                write_memory(adress[: bit[0]] + "1" + adress[bit[0] + 1 :], val, bit[0] + 1, mem)
                return
        mem[int(adress, 2)] = val

    memory1 = {}
    memory2 = {}
    current_mask = ""

    for line in code:
        if line[1] == "a":
            current_mask = re.match(r"mask = (.+)", line).groups()[0]
        elif line[1] == "e":
            adress, val = re.match(r"mem\[(\d+)\] = (\d+)", line).groups()
            new_val = f"{int(val):#038b}"[2:]
            new_adress = f"{int(adress):#038b}"[2:]
            for bit_mask in enumerate(current_mask):
                if bit_mask[1] == "X":
                    new_adress = new_adress[: bit_mask[0]] + "X" + new_adress[bit_mask[0] + 1 :]
                elif bit_mask[1] == "0":
                    new_val = new_val[: bit_mask[0]] + "0" + new_val[bit_mask[0] + 1 :]
                elif bit_mask[1] == "1":
                    new_val = new_val[: bit_mask[0]] + "1" + new_val[bit_mask[0] + 1 :]
                    new_adress = new_adress[: bit_mask[0]] + "1" + new_adress[bit_mask[0] + 1 :]
            memory1[adress] = int(new_val, 2)
            write_memory(new_adress, int(val), 0, memory2)

    print(
        "The sum of values of all non-zero memory adresses in part1 is ",
        sum(memory1.values()),
    )
    print(
        "The sum of values of all non-zero memory adresses in part2 is ",
        sum(memory2.values()),
    )


# https://adventofcode.com/2020/day/15
def day15(input_file):
    def run(times):
        starting_nums = [int(i) for i in input_file.split(",")]
        curr_num = starting_nums[-1]
        num_count = [0 for _ in range(times)]

        for i in enumerate(starting_nums):
            num_count[i[1]] = i[0] + 1

        for i in range(len(starting_nums), times):
            if (prev := num_count[curr_num]) == 0:
                num_count[curr_num] = i
                curr_num = 0
            else:
                num_count[curr_num] = i
                curr_num = i - prev
        return curr_num

    print("The 2020th number is ", run(2020))
    print("The 30000000th number is ", run(30000000))


# https://adventofcode.com/2020/day/16
def day16(input_file):
    inputs = [i.split("\n") for i in input_file.split("\n\n")]

    def create_lambda(lim1l, lim1u, lim2l, lim2u):
        return lambda x: int(lim1l) <= x <= int(lim1u) or int(lim2l) <= x <= int(lim2u)

    rules = {}
    for rule in inputs[0]:
        pattern = r"(.+): (.+)\-(.+) or (.+)\-(.+)"
        name, lim1l, lim1u, lim2l, lim2u = re.match(pattern, rule).groups()
        rules[name] = create_lambda(lim1l, lim1u, lim2l, lim2u)

    def check_rules(ruleset, num):
        for rule in ruleset.values():
            if rule(num):
                return True
        return False

    sum_of_incorrect = 0
    valid_tickets = []
    for ticket in inputs[2][1:]:
        valid_tickets.append(ticket.split(","))
        for number in ticket.split(","):
            if check_rules(rules, int(number)) is True:
                continue
            sum_of_incorrect += int(number)
            valid_tickets.pop()
    print("The sum of incorrect values is", sum_of_incorrect)

    def remove_possibility(poss):
        if len(poss) > 1:
            for rule in poss[1:]:
                rule[1].remove(poss[0][1][0])
            return [poss[0]] + remove_possibility(poss[1:])
        return [poss[0]]

    possibilities = list((k, list(range(len(valid_tickets[0])))) for k, _ in rules.items())
    for ticket in valid_tickets:
        for pos, number in enumerate(ticket):
            for ind, rule in enumerate(rules.values()):
                if not rule(int(number)):
                    possibilities[ind][1].remove(pos)
    possibilities = sorted(possibilities, key=lambda rule: len(rule[1]))
    final_set = remove_possibility(possibilities)

    my_ticket = inputs[1][1].split(",")
    positions_of_departures = 1
    for rule in final_set:
        if rule[0].startswith("departure"):
            positions_of_departures *= int(my_ticket[rule[1][0]])
    print("The sum of the positions of the departure fields is", positions_of_departures)


# https://adventofcode.com/2020/day/17
def day17(input_file):
    w_dimensions = [[[list(i) for i in input_file.split("\n")]]]

    def find_neighbours(w_dimensions, coords):
        result = 0
        for w_inc in range(-1, 2):
            new_w = coords[0] + w_inc
            if -1 < new_w < len(w_dimensions):
                for z_inc in range(-1, 2):
                    new_z = coords[1] + z_inc
                    if -1 < new_z < len(w_dimensions[0]):
                        for y_inc in range(-1, 2):
                            new_y = coords[2] + y_inc
                            if -1 < new_y < len(w_dimensions[0][0]):
                                for x_inc in range(-1, 2):
                                    new_x = coords[3] + x_inc
                                    if -1 < new_x < len(w_dimensions[0][0][0]):
                                        if w_dimensions[new_w][new_z][new_y][new_x] == "#":
                                            result += 1
        return result

    def iteration(w_dimensions):
        active_cubes = 0
        new_w_dimension = []
        for w_coord in range(-1, len(w_dimensions) + 1):
            new_z_planes = []
            for z_coord in range(-1, len(w_dimensions[0]) + 1):
                new_plane = []
                for y_coord in range(-1, len(w_dimensions[0][0]) + 1):
                    new_row = []
                    for x_coord in range(-1, len(w_dimensions[0][0][0]) + 1):
                        try:
                            if -1 in (w_coord, z_coord, y_coord, x_coord):
                                raise IndexError
                            own_state = w_dimensions[w_coord][z_coord][y_coord][x_coord]
                        except IndexError:
                            own_state = "."
                        neigbours = find_neighbours(
                            w_dimensions, [w_coord, z_coord, y_coord, x_coord]
                        )
                        if own_state == "." and neigbours == 3:
                            new_row.append("#")
                            active_cubes += 1
                        elif own_state == ".":
                            new_row.append(".")
                        elif neigbours in (3, 4):  # Always counts itself
                            new_row.append("#")
                            active_cubes += 1
                        else:
                            new_row.append(".")
                    new_plane.append(new_row)
                new_z_planes.append(new_plane)
            new_w_dimension.append(new_z_planes)
        return new_w_dimension, active_cubes

    for _ in range(6):
        w_dimensions, active_cubes = iteration(w_dimensions)

    print(f"At the end of 6 cycles {active_cubes} remain with Hypercube")


# https://adventofcode.com/2020/day/18
def day18(input_file):
    equations = input_file.split("\n")
    result_1 = 0
    result_2 = 0
    ops = {"+": operator.add, "*": operator.mul}

    def collapse(equation, precedence):
        replacements = re.findall(r".* ?\(+([ \d+\*]+?)\)+ ?.*?", equation)
        for index, pattern in enumerate(replacements):
            replacements[index] = (str(calculate(pattern, precedence)), pattern)
        for replace_value, pattern in replacements:
            equation = equation.replace(f"({pattern})", replace_value)
        return equation

    def calculate_precedence(equation):
        equation = equation.split(" ")
        while "+" in equation:
            index = equation.index("+")
            equation[index - 1] = str(int(equation.pop(index - 1)) + int(equation.pop(index)))
        return equation

    def calculate(equation, precedence):
        while "(" in equation:
            equation = collapse(equation, precedence)
        if precedence:
            while "+" in equation:
                equation = calculate_precedence(equation)
        if not isinstance(equation, list):
            equation = equation.split(" ")
        res = int(equation[0])
        for index in range(1, len(equation), 2):
            res = ops[equation[index]](res, int(equation[index + 1]))
        return res

    for equation in equations:
        result_1 += calculate(equation, False)
    print("Sum of all resulting values with normal precedence is", result_1)

    for equation in equations:
        result_2 += calculate(equation, True)
    print("Sum of all resulting values with abnormal precedence is", result_2)


# https://adventofcode.com/2020/day/19
def day19(input_file):
    # Never look at this again ...
    rules, messages = [i.split("\n") for i in input_file.split("\n\n")]
    result_1 = 0

    def split_rules(number, rule, rules_dict):
        if isinstance(rule, re.Pattern):
            return rule
        if '"' in rule:
            pattern = re.compile(rule[1])
            rules_dict[number] = pattern
        elif "|" in rule:
            sub_pattern_1, sub_pattern_2 = rule.split(" | ")
            if number in sub_pattern_2.split(" "):
                sub_rules = sub_pattern_1.split(" ")
                pattern_string = ""
                for index, sub_rule in enumerate(sub_rules):
                    sub_rules[index] = split_rules(None, rules_dict[sub_rule], rules_dict).pattern
                for repeat in range(1, 41):
                    pattern_string += "".join(f"{i}{{{repeat}}}" for i in sub_rules) + "|"
                pattern = re.compile("(" + pattern_string[:-1] + ")")
            else:
                sub_pattern_1 = split_rules(None, sub_pattern_1, rules_dict)
                sub_pattern_2 = split_rules(None, sub_pattern_2, rules_dict)
                pattern = re.compile(
                    f"({'|'.join([sub_pattern_1.pattern, sub_pattern_2.pattern])})"
                )
            if number is not None:
                rules_dict[number] = pattern
        elif " " in rule:
            sub_rules = rule.split(" ")
            for index, sub_rule in enumerate(sub_rules):
                sub_rules[index] = split_rules(sub_rule, rules_dict[sub_rule], rules_dict)
            pattern = re.compile("".join(i.pattern for i in sub_rules))
            if number is not None:
                rules_dict[number] = pattern
        else:
            pattern = split_rules(rule, rules_dict[rule], rules_dict)
        return pattern

    rules = dict([k.split(": ") for k in rules])
    for number, rule in rules.items():
        split_rules(number, rule, rules)

    for message in messages:
        stripped_message = rules["0"].sub("", message)
        if stripped_message == "":
            result_1 += 1
    print("Messages following rule 0 is", result_1)

    # Question 2
    rules, messages = [i.split("\n") for i in input_file.split("\n\n")]
    result_2 = 0
    rules = dict([k.split(": ") for k in rules])
    rules["8"] = "42 | 42 8"
    rules["11"] = "42 31 | 42 11 31"

    for number, rule in rules.items():
        split_rules(number, rule, rules)

    for message in messages:
        if rules["0"].fullmatch(message):
            result_2 += 1
    print("All correct messages with updated rules are", result_2)


def solver(day):
    start = time.time()
    with open(INPUT_FILES[day], "r") as file:
        globals()[day](file.read())
    print(f"Execution of solution for {day} took {round((time.time() - start) * 1000, 5)} ms")


def all_days():
    totaltime = time.time()
    for i in range(19):
        print(f"===== DAY {i+1:2d} =====")
        solver(f"day{i+1}")
        print()
    print(f"Execution of all solutions took {round((time.time() - totaltime) * 1000, 5)} ms")


if __name__ == "__main__":
    solver("day19")
    # all_days()
