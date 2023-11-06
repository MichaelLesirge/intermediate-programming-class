import enum

class Color(str, enum.Enum):
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    NONE = ''


class Modifier(str, enum.Enum):
    RESET_ALL = "\033[0m"
    
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALICS = '\033[3m'
    UNDERLINE = '\033[4m'
    
    INVERT = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'
    DOUBLE_UNDERLINE = '\033[21m'
    

def make_color(text: str, color: Color, modifiers: list[Modifier] = []) -> str:
    return f"{color.value}{"".join(modifier.value for modifier in modifiers)}{text}{Modifier.RESET_ALL.value}"
    