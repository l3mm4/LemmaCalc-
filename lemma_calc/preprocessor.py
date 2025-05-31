import re


def replace_exponentiation(expr):
    """Replace '^' with '**' for exponentiation."""
    return expr.replace("^", "**")


def insert_implicit_multiplication(expr):
    """
    Insert '*' where implicit multiplication is assumed, e.g.:
    - between number and parenthesis: 2(3) => 2*(3)
    - between closing parenthesis and number or identifier: (2)3 => (2)*3, (2)pi => (2)*pi
    - between number and identifier: 2pi => 2*pi
    """
    expr = re.sub(r"(\d)(\()", r"\1*\2", expr)
    expr = re.sub(r"(\))(\d|[a-zA-Z_])", r"\1*\2", expr)
    expr = re.sub(r"(\d)([a-zA-Z_])", r"\1*\2", expr)
    return expr


def handle_factorial(expr):
    """
    Replace 'n!' with 'factorial(n)' including expressions in parentheses.
    Examples:
        5! -> factorial(5)
        (2+3)! -> factorial((2+3))
    """
    expr = re.sub(r"(\([^()]*\))!", r"factorial\1", expr)
    expr = re.sub(r"(\d+)!", r"factorial(\1)", expr)
    return expr


def preprocess_expression(expr):
    """Run all preprocessing functions in sequence."""
    for func in [
        replace_exponentiation,
        insert_implicit_multiplication,
        handle_factorial,
    ]:
        expr = func(expr)
    return expr
