# lemma_calc/constants.py


import math
import operator
import ast


HISTORY_FILE = "history.json"
VERSION = "0.4"


# Allowed math functions accessible to the user
allowed_names = {
    "factorial": math.factorial,
    "abs": abs,
    "round": round,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,  # new
    "acos": math.acos,  # new
    "atan": math.atan,  # new
    "degrees": math.degrees,  # new
    "radians": math.radians,  # new
    "log": math.log,  # natural log
    "log10": math.log10,  # base-10 log
    "sqrt": math.sqrt,
    "exp": math.exp,
    "floor": math.floor,
    "ceil": math.ceil,
}


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
