import sexpdata

from evaluate_tree import evaluate_tree


def evaluate_expression(expression, input_vector):
    if type(input_vector) == str:
        input_vector = tuple(float(x) for x in input_vector.strip().split())
    syntax_tree = sexpdata.loads(expression)
    result = evaluate_tree(syntax_tree, input_vector)
    return result