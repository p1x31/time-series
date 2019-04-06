import random

from solution import Solution
from math_functions import MATH_FUNCTIONS
from data_functions import DATA_FUNCTIONS
from tree import Tree

MAX_DEPTH = 10


def random_number(hi=0, lo=0):
    return random.randrange(lo, hi)


def random_function():
    return random.choice([*MATH_FUNCTIONS.items(), *DATA_FUNCTIONS.items()])


def create_random_node(depth=0, max_depth=MAX_DEPTH):
    if max_depth <= 0 or random.random() < depth / max_depth:
        return Tree(random_number(MAX_DEPTH))
    name, (_, arity) = random_function()
    return Tree([name, *create_random_nodes(arity, depth + 1, max_depth)])


def create_random_nodes(num_nodes, depth=0, max_depth=MAX_DEPTH):
    return [create_random_node(depth, max_depth) for _ in range(num_nodes)]


def generate_random_solutions(n, input_size, max_depth=MAX_DEPTH):
    """
    Generate random functions of input data.
    :param n: The number of random solutions to generate.
    :param input_size: The size of each input vector.
    :param max_depth: The maximum depth of any expression tree.
    :return: A sequence of random, *valid* expressions.
    """
    return [Solution(node) for node in create_random_nodes(n, max_depth=max_depth)]