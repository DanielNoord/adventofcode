# Solution to AoC 2020 day 3

# Load Map file
MAP = []
file = open("input.txt", "r")
for line in file:
    MAP.append(line.replace("\n", ""))
file.close()
MAP_WIDTH = len(MAP[0])

def check_trees(vertical, horizontal):
    pointer = [0, 0]
    trees = 0
    for _ in range(0, len(MAP) - 1, vertical):
        pointer[0] += vertical
        pointer[1] += horizontal
        if MAP[pointer[0]][pointer[1] % MAP_WIDTH] == "#":
            trees += 1
    print(f"With a slope of {horizontal} right and {vertical} down you will encounter {trees} trees")
    return trees

if __name__ == "__main__":
    check_trees(1, 3)
    print(check_trees(1, 1) * check_trees(1, 3) * check_trees(1, 5) * check_trees(1, 7) * check_trees(2, 1))
