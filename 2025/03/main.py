from __future__ import annotations

from utils.io import read_input_lines

YEAR = 2025
DAY = 3


def parse_input(lines: list[str]) -> list[str]:
    """Return the non-empty battery banks as strings of digits."""

    return [line.strip() for line in lines if line.strip()]


def _max_joltage_k_digits(bank: str, k: int) -> int:
    """Return the largest joltage that uses exactly ``k`` digits in order.

    The algorithm uses a monotonic stack and runs in O(n) time. Digits stay in order
    and cannot be rearranged.
    """

    digits = [int(ch) for ch in bank.strip()]
    if len(digits) < k:
        raise ValueError(f"Bank must contain at least {k} batteries")

    drops = len(digits) - k
    stack: list[int] = []

    for d in digits:
        while drops and stack and stack[-1] < d:
            stack.pop()
            drops -= 1
        stack.append(d)

    if drops:
        stack = stack[:-drops]

    result = 0
    for d in stack[:k]:
        result = result * 10 + d
    return result


def max_bank_joltage(bank: str) -> int:
    """Return the maximum two-digit joltage that can be formed from a bank."""

    return _max_joltage_k_digits(bank, 2)


def part1(banks: list[str]) -> int:
    """Sum the maximum joltage obtainable from each bank."""

    return sum(max_bank_joltage(bank) for bank in banks)


def part2(banks: list[str]) -> int:
    """Sum the maximum 12-digit joltage obtainable from each bank."""

    return sum(_max_joltage_k_digits(bank, 12) for bank in banks)


def run(variant: str | None = None) -> None:
    """Read the input and print both answers."""

    lines = read_input_lines(YEAR, DAY, variant)
    banks = parse_input(lines)
    print(f"Part 1: {part1(banks)}")
    print(f"Part 2: {part2(banks)}")


if __name__ == "__main__":
    run()
