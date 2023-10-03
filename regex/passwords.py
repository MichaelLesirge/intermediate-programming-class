import re
import pathlib

path = pathlib.Path(__file__).parent

def find_all(pattern: re.Pattern[str], strings: list[str]) -> dict[int, str]:
    return [line for line in strings if re.match(pattern, line)]

def find_all_ranked(pattern: re.Pattern[str], strings: list[str]) -> list[str]:
    return {rank: line for rank, line in enumerate(strings) if re.match(pattern, line)}

with open(path / "password.txt", "r") as file:
    lines = [line.rstrip("\n") for line in file.readlines()]

top_n = 10

pattern = r"[A-Z][a-z]+\d+"
matches = find_all_ranked(pattern, lines)

print(f"{len(matches)} matches for pattern in list of {len(lines)}. That is {len(matches)/len(lines):.1%} of passwords on the list.")

print(f"Showing top {top_n} passwords that match.")
for relative_rank, (rank, line) in enumerate(matches.items()):
    if relative_rank >= top_n: break
    print(f"#{relative_rank + 1}: {line} (overall rank of {rank + 1})")