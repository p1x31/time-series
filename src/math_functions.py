import operator
import math

from safety_harness import safety_harness
from function import Function


def ifleq(a, b, c, d):
    return c if a <= b else d


def limited_pow(a, b):
    """
    Define a "limited" version of pow, which doesn't allow powers greater
    than 1024. This seems small, but note that 2 ** (2 ** 10) is a number
    309 digits long.
    """
    if a == 1 or b == 0:
        return 1
    if a == 0:
        return 0
    if b > 32:
        return a ** 32
    if a > 1024 and b > 1024:
        return 1024 ** 1024
    return pow(a, b)


def limited_exp(x):
    """
    Define a "limited" version of exp, which doesn't allow powers greater
    than 128. As above, this is fast.
    """
    if x > 128:
        return 0
    return math.exp(x)


MATH_FUNCTIONS = {
    "add": Function(operator.add, arity=2),
    "sub": Function(operator.sub, arity=2),
    "mul": Function(operator.mul, arity=2),
    "div": Function(operator.truediv, arity=2),
    "pow": Function(limited_pow, arity=2),
    "sqrt": Function(math.sqrt, arity=1),
    "log": Function(math.log2, arity=1),
    "exp": Function(limited_exp, arity=1),
    "max": Function(max, arity=2),
    "ifleq": Function(ifleq, arity=4)
}


for key, function in MATH_FUNCTIONS.items():
    MATH_FUNCTIONS[key] = safety_harness(function)


def lazy_evaluate(fn, params):
    """
    Check a lot of special-cases which allow us to cut a parameter
    list down in size without evaluating the parameters.
    """

    if fn == "add":
        if params[0] == 0:
            return params[1]
        if params[1] == 0:
            return params[0]
    elif fn == "sub":
        if params[1] == 0:
            return params[0]
    elif fn == "mul":
        if params[0] == 0:
            return 0
        elif params[1] == 0:
            return 0
        elif params[0] == 1:
            return params[1]
        elif params[1] == 1:
            return params[0]
    elif fn == "div":
        if params[0] == 0:
            return params[0]
        elif params[1] == 0:
            return 0
        elif params[1] == 1:
            return params[0]
    elif fn == "pow":
        if params[1] == 0:
            return 1
        if params[0] in (0, 1):
            return params[0]
    elif fn == "ifleq":
        try:
            if params[0] <= params[1]:
                return params[2]
            else:
                return params[3]
        except TypeError:
            pass

    # If none of these apply, return the original parameter list.
    return [fn, *params]