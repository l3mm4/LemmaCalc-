# lemma_calc/prompt_utils.py

from prompt_toolkit.completion import WordCompleter
import threading
import sys
import time
import os

# Allowed function names for tab-completion (used in the input prompt)
allowed_names = {
    "sin": None,
    "cos": None,
    "tan": None,
    "sqrt": None,
    "log": None,
    # Add all additional supported functions here...
}

# Combine functions, constants, and commands for auto-completion
function_completions = list(
    set(list(allowed_names.keys()) + ["pi", "e", "history", "clear", "q"])
)

# Create a WordCompleter instance for prompt_toolkit
completer = WordCompleter(function_completions, ignore_case=True)


def wait_for_keypress_or_timeout(timeout, event):
    """
    Wait for a keypress or until timeout expires.

    Args:
        timeout (float): Time in seconds to wait.
        event (threading.Event): Event to set if a key is pressed.

    This function runs a thread that waits for a keypress on both Windows
    and Unix systems. If a key is pressed or timeout occurs, it sets the event.
    """

    def worker():
        try:
            if sys.platform == "win32":
                import msvcrt

                start = time.time()
                while time.time() - start < timeout:
                    if msvcrt.kbhit():
                        msvcrt.getch()
                        event.set()
                        break
                    time.sleep(0.1)
            else:
                import select

                rlist, _, _ = select.select([sys.stdin], [], [], timeout)
                if rlist:
                    sys.stdin.read(1)
                    event.set()
        except Exception:
            pass  # Fail silently if input can't be read

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()


def supports_ansi():
    """
    Check whether the current terminal supports ANSI escape codes.

    Returns:
        bool: True if ANSI is supported, False otherwise.
    """
    return sys.stdout.isatty() and os.name != "nt"


def typewriter_print(text, delay=0.01, skip_event=None, color=None):
    """
    Print text with a typewriter-style animation effect.

    Args:
        text (str): The text to print.
        delay (float): Delay between characters (default: 0.01s).
        skip_event (threading.Event, optional): If set, bypasses animation delay.
        color (str, optional): ANSI color code to use (e.g., "\\033[92m" for green).

    If the terminal does not support ANSI, or no color is given, plain text is printed.
    """
    use_color = supports_ansi() and color is not None
    if use_color:
        sys.stdout.write(color)
        sys.stdout.flush()

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if skip_event and skip_event.is_set():
            continue
        time.sleep(delay)

    if use_color:
        sys.stdout.write("\033[0m")  # Reset color
        sys.stdout.flush()

    print()  # Final newline after animation
