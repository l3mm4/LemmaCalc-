# lemma_calc.core.py

import re
import ast
import math
import re
from .constants import allowed_names, allowed_operators

# Dictionary to store user variables
variables = {}


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


def insert_implicit_multiplication(expr):
    """
    Insert explicit multiplication operator '*' for cases like:
    3(4+2), (2+3)4, or 5!(22)
    """
    expr = re.sub(r"(\d+|\))\s*\(", r"\1*(", expr)
    expr = re.sub(r"\)\s*(\d+|factorial)", r")*\1", expr)
    return expr


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
