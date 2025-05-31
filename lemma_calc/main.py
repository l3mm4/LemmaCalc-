# lemma_calc.main.py

import threading
from prompt_toolkit import prompt
from .display import Colors
from .prompt_utils import completer, wait_for_keypress_or_timeout
from .display import print_banner, print_instructions, clear_screen
from .core import evaluate_expression, format_result, process_assignment
from .history import load_history, save_history
from .core_utils import handle_command_line_args, show_doc
from datetime import datetime


def main():
    skip_event = threading.Event()
    print("Press any key to skip the intro...")
    wait_for_keypress_or_timeout(5, skip_event)
    print_banner(skip_event)
    print_instructions()
    variables = {}
    history = load_history()

    while True:
        try:
            user_input = prompt(
                "\nEnter calculation (or 'q' to quit): ", completer=completer
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"{Colors.BOLD}{Colors.RED}Unexpected error:{Colors.RESET} {e}")
            continue

        if user_input.lower() == "q":
            print("Goodbye!")
            break

        if user_input.lower() == "clear":
            clear_screen()
            print_banner(skip_event=None)
            print_instructions()
            continue

        if user_input.lower() == "history":
            if not history:
                print("No history yet.")
            else:
                print("History:")
                for i, (ts, expr, res) in enumerate(history, 1):
                    print(
                        f"{Colors.BOLD}{i}.{Colors.RESET} [{Colors.DIM}{ts}{Colors.RESET}] {expr} = {Colors.GREEN}{res}{Colors.RESET}"
                    )
            continue

        if user_input.lower() == "man":
            show_doc("man.txt")
            continue

        if user_input.lower() == "tldr":
            show_doc("tldr.txt")
            continue

        if user_input == "":
            continue

        # Split input by semicolons for multi-expression support
        expressions = [expr.strip() for expr in user_input.split(";") if expr.strip()]

        for expr in expressions:
            try:
                # Evaluate expression or handle assignment
                result = None
                assignment_result = process_assignment(expr, variables)
                if assignment_result is not None:
                    print(assignment_result)
                    history.append(
                        (
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            expr,
                            assignment_result,
                        )
                    )
                else:
                    result = evaluate_expression(expr, variables)
                    formatted = format_result(result)
                    print(f"Result: {formatted}")
                    history.append(
                        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), expr, formatted)
                    )
            except Exception as e:
                print(f"{Colors.BOLD}{Colors.RED}Error:{Colors.RESET} {e}")

    save_history(history)


if __name__ == "__main__":
    handle_command_line_args()
    main()
