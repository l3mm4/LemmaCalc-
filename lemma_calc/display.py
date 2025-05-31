# lemma_calc/display.py

from .prompt_utils import typewriter_print
import os


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[36m"
    YELLOW = "\033[33m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    UNDERLINE = "\033[4m"


def clear_screen():
    """Clear the terminal screen for both Windows and Unix-like systems."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner(skip_event):
    """
    Display the stylized LemmaCalc™ banner using a typewriter-style effect.
    """
    banner = r"""
╔════════════════════════════════════════════════════════════════════════════╗
║   ██╗     ███████╗███╗   ███╗███╗   ███╗ █████╗       ▲                    ║
║   ██║     ██╔════╝████╗ ████║████╗ ████║██╔══██╗     ▲ ▲                   ║
║   ██║     █████╗  ██╔████╔██║██╔████╔██║███████║    ▲ ▲ ▲                  ║
║   ██║     ██╔══╝  ██║╚██╔╝██║██║╚██╔╝██║██╔══██║   ▲ ▲ ▲ ▲                 ║
║   ███████╗███████╗██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║       LemmaCalc™ v0.5     ║
║   ╚══════╝╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝     Powered by Python 3   ║
╚════════════════════════════════════════════════════════════════════════════╝
"""
    typewriter_print(banner, delay=0.002, skip_event=skip_event, color=Colors.GREEN)


def print_instructions():
    """Display instructions for using LemmaCalc™."""
    Y = Colors.YELLOW
    B = Colors.BOLD
    R = Colors.RESET

    instructions = f"""
{B}{Y}    Instructions:{R}
    - Enter any mathematical expression using +, -, *, /, %, ** operators.
    - Use parentheses to group expressions, e.g. (2 + 3) * 4.
    - Factorials can be used by appending '!' to integers or expressions, e.g. 5! or (2+3)!.
    - '^' can be used as shorthand for exponentiation, e.g. 2^3 = 8.
    - Implicit multiplication is supported: 3(2+1), (2+3)4, or 5!(22).
    - Supports functions: sin, cos, tan, asin, acos, atan, log, log10, sqrt,
      exp, floor, ceil, abs, round, factorial, degrees, radians.
    - Constants: pi, e
    - End expressions with '=' if desired (optional).
    - {B}Type 'history'{R} to view past results.
    - {B}Type 'clear'{R} to clear the screen.
    - {B}Type 'q'{R} to quit.
    """
    print(instructions)
