import operator
import math

from safety_harness import safety_harness


MATH_FUNCTIONS = {
    "add": operator.add,
    "sub": operator.sub,
    "mul": operator.mul,
    "div": operator.truediv,
    "pow": operator.pow,
    "sqrt": math.sqrt,
    "log": math.log2,
    "exp": math.exp,
    "max": max,
    "ifleq": lambda a, b, c, d: c if a <= b else d
}


for key, function in MATH_FUNCTIONS.items():
    MATH_FUNCTIONS[key] = safety_harness(function) 