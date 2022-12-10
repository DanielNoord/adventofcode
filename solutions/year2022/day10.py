from __future__ import annotations


def part1(data: str) -> str | int:
    cycle, register, interesting_scores = -20, 1, 0

    for instruction in data.splitlines():
        cycle += 1
        if not cycle % 40:
            interesting_scores += register * (20 + cycle)
        if instruction[0] == "a":
            cycle += 1
            if not cycle % 40:
                interesting_scores += register * (20 + cycle)
            register += int(instruction[4:])
    return interesting_scores


def part2(data: str) -> str | int:
    pixels: list[str] = []
    instructions = data.splitlines()
    instruction_count = 0
    register: tuple[int, int, int] = (0, 1, 2)
    bump: int | None = None

    for y_coord in range(6):
        pixels.append("")
        for x_coord in range(40):
            if x_coord in register:
                pixels[y_coord] += "#"
            else:
                pixels[y_coord] += "."

            if bump is not None:
                register = (register[0] + bump, register[1] + bump, register[2] + bump)
                bump = None
                instruction_count += 1
                continue

            instruction = instructions[instruction_count]
            if instruction[0] == "n":
                instruction_count += 1
            elif instruction[0] == "a":
                bump = int(instruction[4:])

    return "\n".join(pixels)
