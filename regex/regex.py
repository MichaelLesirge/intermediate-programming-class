import re
import pathlib
import sys

path = pathlib.Path(__file__).parent

def find_all(pattern: re.Pattern[str], strings: list[str]) -> dict[int, str]:
    return [line for line in strings if re.match(pattern, line)]

def find_all_ranked(pattern: re.Pattern[str], strings: list[str]) -> dict[int, str]:
    return {rank: line for rank, line in enumerate(strings) if re.match(pattern, line)}

def print_ranked(rankings: dict[int, str], top_n: int = float("inf")):
    for relative_rank, (rank, line) in enumerate(rankings.items()):
        if relative_rank >= top_n: break
        print(f"#{relative_rank + 1}: {line} (overall rank of {rank + 1})")
    

with open(path / "password.txt", "r") as file:
    lines = [line.rstrip("\n") for line in file]

pattern = r"^[a-z]+\d+$"
matches = find_all_ranked(pattern, lines)
print_ranked(matches, top_n=100)