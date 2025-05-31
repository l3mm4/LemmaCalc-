# lemma_calc/input_handler.py

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import os
import threading
import time
import sys

__all__ = [
    "set_completions",
    "typewriter_print",
    "wait_for_keypress_or_timeout",
    "get_input",
]


# Default values (can be overridden from main)
function_completions = []
completer = None


def set_completions(words):
    global function_completions, completer
    function_completions = words
    completer = WordCompleter(function_completions, ignore_case=True)


def typewriter_print(text, delay=0.03, skip_event=None, color=""):
    """
    Print text with typewriter effect.
    If skip_event is set during printing, print the rest immediately.
    """
    if color:
        text = f"{color}{text}\033[0m"  # Wrap text with color and reset
    for char in text:
        if skip_event and skip_event.is_set():
            print(text[text.index(char) :], end="", flush=True)
            break
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def wait_for_keypress_or_timeout(timeout, skip_event):
    """
    Wait for a key press or timeout.
    On Windows uses msvcrt.kbhit(); on other OSes, waits for Enter input with a thread.
    Sets skip_event when input is detected or timeout expires.
    """

    def wait_input():
        try:
            input()
            skip_event.set()
        except EOFError:
            pass

    if os.name == "nt":
        try:
            import msvcrt

            start = time.time()
            while time.time() - start < timeout:
                if msvcrt.kbhit():
                    msvcrt.getch()
                    skip_event.set()
                    break
                time.sleep(0.05)
        except Exception as e:
            print(f"Warning: msvcrt failed ({e})")
    else:
        print(f"Press Enter to skip the intro... (waiting {timeout} seconds)")
        thread = threading.Thread(target=wait_input)
        thread.daemon = True
        thread.start()
        thread.join(timeout)


def get_input():
    """Prompt user for input using prompt_toolkit."""
    if completer is None:
        return prompt("Enter expression: ")
    return prompt("Enter expression: ", completer=completer)
