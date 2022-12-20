from __future__ import annotations

# pylint: disable=compare-to-zero


def _do_round(
    original_sequence: list[tuple[int, int]],
    current_sequence: list[tuple[int, int]],
    len_sequence: int,
) -> tuple[list[tuple[int, int]], tuple[int, int]]:
    zero_pair = None

    for number in original_sequence:
        if number[1] == 0:
            zero_pair = number

        index = current_sequence.index(number)
        current_sequence.pop(index)
        new_index = (index + number[1]) % (len_sequence - 1)

        # Wrap around if needed
        if new_index == 0:
            new_index = len_sequence - 1
        elif new_index == len_sequence - 1:
            new_index = 0

        current_sequence = (
            current_sequence[:new_index] + [number] + current_sequence[new_index:]
        )

    assert zero_pair
    return current_sequence, zero_pair


def _get_answer(
    current_sequence: list[tuple[int, int]],
    zero_pair: tuple[int, int],
    len_sequence: int,
) -> int:
    index_zero = current_sequence.index(zero_pair)
    thousand_index = (index_zero + 1000) % len_sequence
    two_thousand_index = (index_zero + 2000) % len_sequence
    three_thousand_index = (index_zero + 3000) % len_sequence
    return (
        current_sequence[thousand_index][1]
        + current_sequence[two_thousand_index][1]
        + current_sequence[three_thousand_index][1]
    )


def part1(data: str) -> str | int:
    original_sequence = [(i, int(x)) for i, x in enumerate(data.splitlines())]
    len_sequence = len(original_sequence)
    current_sequence, zero_pair = _do_round(
        original_sequence, original_sequence.copy(), len_sequence
    )
    return _get_answer(current_sequence, zero_pair, len_sequence)


def part2(data: str) -> str | int:
    original_sequence = [
        (i, int(x) * 811589153) for i, x in enumerate(data.splitlines())
    ]
    len_sequence = len(original_sequence)
    current_sequence = original_sequence.copy()
    for _ in range(10):
        current_sequence, zero_pair = _do_round(
            original_sequence, current_sequence, len_sequence
        )

    return _get_answer(current_sequence, zero_pair, len_sequence)
