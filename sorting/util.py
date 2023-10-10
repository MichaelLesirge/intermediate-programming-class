import random

def make_random(length: int, num_range: tuple[int, int] = None) -> list[int]:
    array = [(random.randint(*num_range) + 1 if num_range else i) for i in range(length)]
    if num_range is None: random.shuffle(array)
    return array