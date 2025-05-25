# Sean Jette
# Python Calculator v0.4

import ast
import operator
import math
import re

# import sys
import time
import threading
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import difflib  # For close function name matching

# Allowed math functions accessible to the user
allowed_names = {
    "factorial": math.factorial,
    "abs": abs,
    "round": round,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,  # natural log
    "log10": math.log10,  # base-10 log
    "sqrt": math.sqrt,
    "exp": math.exp,
    "floor": math.floor,
    "ceil": math.ceil,
    # Add more functions here if needed
}

# Setup auto-completion with function names, constants, and commands
function_completions = list(
    set(list(allowed_names.keys()) + ["pi", "e", "history", "clear", "q"])
)
completer = WordCompleter(function_completions, ignore_case=True)

# Allowed operators for safe evaluation
allowed_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}
# Dictionary to store user variables
variables = {}


def main():
    skip_event = threading.Event()
    print("Press any key to skip the intro...")
    wait_for_keypress_or_timeout(5, skip_event)
    print_banner(skip_event)
    print_instructions()

    history = []

    while True:
        try:
            user_input = prompt(
                "\nEnter calculation (or 'q' to quit): ", completer=completer
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
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
                for i, (expr, res) in enumerate(history, 1):
                    print(f"{i}: {expr} = {res}")
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
                    history.append((expr, assignment_result))
                else:
                    result = evaluate_expression(expr, variables)
                    formatted = format_result(result)
                    print(f"Result: {formatted}")
                    history.append((expr, formatted))
            except Exception as e:
                print(f"Error: {e}")


def safe_eval(node):
    """
    Recursively evaluate the parsed AST nodes in a safe manner,
    allowing only predefined operators and functions.
    """
    if isinstance(node, ast.Expression):
        return safe_eval(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError(f"Invalid constant {node.value}")

    elif isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op_type = type(node.op)
        if op_type in allowed_operators:
            return allowed_operators[op_type](left, right)
        else:
            raise ValueError(f"Operator {op_type} not allowed")

    elif isinstance(node, ast.UnaryOp):
        operand = safe_eval(node.operand)
        op_type = type(node.op)
        if op_type in allowed_operators:
            return allowed_operators[op_type](operand)
        else:
            raise ValueError(f"Unary operator {op_type} not allowed")

    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in allowed_names:
                raise ValueError(f"Function {func_name} unknown or not allowed")
            func = allowed_names[func_name]
            args = [safe_eval(arg) for arg in node.args]
            if node.keywords:
                raise ValueError("Keyword arguments not allowed")

            # Specific check for factorial:
            if func_name == "factorial":
                if len(args) != 1:
                    raise ValueError("factorial() takes exactly one argument")
                arg_val = args[0]
                if not (isinstance(arg_val, int) and arg_val >= 0):
                    raise ValueError(
                        "factorial() only defined for non-negative integers"
                    )

            return func(*args)
        else:
            raise ValueError("Invalid function call")

    elif isinstance(node, ast.Name):
        var_name = node.id
        if var_name in variables:
            return variables[var_name]
        elif var_name in ["pi", "e"]:
            # Return math constants if used directly (just in case)
            return {"pi": math.pi, "e": math.e}[var_name]
        else:
            raise ValueError(f"Unknown variable or identifier {var_name}")

    else:
        raise ValueError(f"Unsupported expression: {type(node)}")


def parse_factorials(expr):
    """
    Convert all occurrences of n! or (expr)! into factorial(expr)
    so the safe_eval can handle them as function calls.
    """
    pattern = re.compile(r"(\([^()]+\)|\d+)!")

    while True:
        match = pattern.search(expr)
        if not match:
            break
        inner = match.group(1)
        replacement = f"factorial({inner})"
        expr = expr[: match.start()] + replacement + expr[match.end() :]
    return expr


def insert_implicit_multiplication(expr):
    """
    Insert explicit multiplication operator '*' for cases like:
    3(4+2), (2+3)4, or 5!(22)
    """
    expr = re.sub(r"(\d+|\))\s*\(", r"\1*(", expr)
    expr = re.sub(r"\)\s*(\d+|factorial)", r")*\1", expr)
    return expr


def preprocess_expression(expr):
    """
    Prepare the input expression:
    - Remove spaces
    - Remove trailing '=' if present
    - Replace '^' with '**'
    - Replace 'pi' and 'e' only when they appear as whole words
    - Parse factorials and implicit multiplication
    """
    expr = expr.replace(" ", "")
    if expr.endswith("="):
        expr = expr[:-1]
    expr = expr.replace("^", "**")

    # Replace constants only when they appear as whole words
    expr = re.sub(r"\bpi\b", f"({math.pi})", expr)
    expr = re.sub(r"\be\b", f"({math.e})", expr)

    expr = parse_factorials(expr)
    expr = insert_implicit_multiplication(expr)
    return expr


def process_assignment(expr, variables):
    """
    Detect assignment expressions of the form: var = expression
    If assignment found, evaluate the right-hand side expression,
    store result in variables dictionary, and return None (no print).
    If no assignment, return None.
    """
    # Match variable = expression, variable must be valid Python identifier
    match = re.match(r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$", expr)
    if match:
        var_name = match.group(1)
        rhs_expr = match.group(2)
        result = evaluate_expression(rhs_expr, variables)
        variables[var_name] = result
        return f"{var_name} = {format_result(result)}"
    else:
        return None


def evaluate_expression(expr, variables):
    """
    Evaluate the user input expression safely after preprocessing.
    Enhanced error handling for user-friendly messages.

    Steps:
    - Replace variables in expr with their values from the variables dict.
    - Preprocess expression (handle factorial, ^, implicit mult, etc.).
    - Parse and safely evaluate the expression AST.
    """
    # Replace variable names in the expression with their values
    for var_name, var_value in variables.items():
        # Replace whole word occurrences of var_name with its value as string
        # Use word boundaries so 'x' doesn't replace parts of other words
        expr = re.sub(rf"\b{re.escape(var_name)}\b", str(var_value), expr)

    expr = preprocess_expression(expr)

    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError:
        raise ValueError(
            "Syntax error: please check your expression for invalid syntax."
        )

    try:
        result = safe_eval(tree)
        return result
    except ZeroDivisionError:
        raise ValueError("Math error: division by zero is undefined.")
    except ValueError as ve:
        # Enhance unknown function errors
        msg = str(ve)
        if "Function" in msg and "unknown or not allowed" in msg:
            unknown_func = msg.split()[1]
            suggestions = difflib.get_close_matches(
                unknown_func, allowed_names.keys(), n=3, cutoff=0.6
            )
            suggestion_text = (
                f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
            )
            raise ValueError(
                f"Function error: unknown function '{unknown_func}'.{suggestion_text}"
            )
        raise
    except TypeError as te:
        raise ValueError(f"Type error: {te}")
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")


def format_result(result):
    """
    Format the result for output:
    - Integers are formatted with commas
    - Floats with integer value are converted to int and formatted
    - Other floats formatted with commas
    """
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    if isinstance(result, int):
        return f"{result:,}"
    else:
        return f"{result:,}"


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_instructions():
    """Print user instructions."""
    instructions = """
Instructions:
- Enter any mathematical expression using +, -, *, /, %, ** operators.
- You can use parentheses for grouping, e.g. (2 + 3) * 4.
- For factorial, type a non-negative integer or expression followed by '!', e.g. 5! or (2+3)!.
- You can use ^ as exponentiation, e.g. 2^3 = 8.
- You can write implicit multiplication like 3(2+1), (2+3)4, or 5!(22).
- Supports functions: sin, cos, tan, log, log10, sqrt, exp, floor, ceil, abs, round, factorial.
- Constants: pi, e
- End expressions with '=' if you want (optional).
- Type 'history' to see past results.
- Type 'clear' to clear the screen.
- Type 'q' at any time to quit.
"""
    print(instructions)


def typewriter_print(text, delay=0.03, skip_event=None):
    """
    Print text with typewriter effect.
    If skip_event is set during printing, print the rest immediately.
    """
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


def print_banner(skip_event):
    """
    Display the stylized calculator banner with a typewriter effect.
    """
    banner = r"""
╔════════════════════════════════════════════════════════════════════════════╗
║   ██╗     ███████╗███╗   ███╗███╗   ███╗ █████╗       ▲                    ║
║   ██║     ██╔════╝████╗ ████║████╗ ████║██╔══██╗     ▲ ▲                   ║
║   ██║     █████╗  ██╔████╔██║██╔████╔██║███████║    ▲ ▲ ▲                  ║
║   ██║     ██╔══╝  ██║╚██╔╝██║██║╚██╔╝██║██╔══██║   ▲ ▲ ▲ ▲                 ║
║   ███████╗███████╗██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║       LemmaCalc™ v0.4     ║
║   ╚══════╝╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝     Powered by Python 3   ║
╚════════════════════════════════════════════════════════════════════════════╝
"""
    typewriter_print(banner, delay=0.002, skip_event=skip_event)


if __name__ == "__main__":
    main()
