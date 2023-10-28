import enum

class Color(str, enum.Enum):
    RED = "\u001b[31m"
    BLUE = "\u001b[34m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m"
    MAGENTA = "\u001b[35m"
    CYAN = "\u001b[36m"
    WHITE = "\u001b[37m"
    BLACK = "\u001b[30m"

STR_BOLD_CODE = "\033[1m"
STR_RESET_CODE = "\033[0m"

def make_color(text: str, color: Color, make_bold = True) -> str:
    return f"{color.value}{STR_BOLD_CODE if make_bold else ""}{text}{STR_RESET_CODE}"