def swap(l: list, a: int, b: int):
    l[a], l[b] = l[b], l[a]

# class Marker(enum.Enum):
class Marker():
    PRIMARY = "blue"
    DONE = "green"
    
    # LEFT_POINTER = ""
    # RIGHT_POINTER = ""