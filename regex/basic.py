import re
import pathlib

path = pathlib.Path(__file__).parent

with open(path / "shakespear.txt", "r") as file:
    text = file.read()

pattern = r"\w+'\w+"
matches = re.findall(pattern, text)


case_insensitive_set = {match.lower() for match in matches}

print(f"{len(matches)} matches with {len(case_insensitive_set)} case insensitive unique values.")
print(case_insensitive_set)