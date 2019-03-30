from math_functions import MATH_FUNCTIONS
from data_functions import DATA_FUNCTIONS


def evaluate_tree(syntax_tree, input_vector):
    if type(syntax_tree) == int:
        return syntax_tree

    if type(syntax_tree) == list:
        fun_key = syntax_tree[0].value()

        params = (evaluate_tree(param, input_vector) for param in syntax_tree[1:])

        if fun_key in MATH_FUNCTIONS:
            fun = MATH_FUNCTIONS[fun_key]
            return fun(*params)

        elif fun_key in DATA_FUNCTIONS:
            fun = DATA_FUNCTIONS[fun_key]
            return fun(*params, input_vector)

        raise ValueError("Invalid function: ", fun_key)