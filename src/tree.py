from parsing import parse
from math_functions import MATH_FUNCTIONS, lazy_evaluate
from data_functions import DATA_FUNCTIONS


class Tree:

    def __init__(self, expression):
        # Parse any raw string expressions.

        assert type(expression) is not type(self)

        if type(expression) is str:
            expression = parse(expression)

        # Use immutable data structures for speed & safety.
        if type(expression) is list:
            expression = tuple(expression)

        self._expression = expression
        self._length = None
        self._string = None
        self._length = self._calculate_length()
        self._string = self._calculate_string()
        self.height = self._calculate_height()

    def evaluate(self, input_vector=None):
        """
        Evaluate a tree's value given a vector of input data.
        :param input_vector: The given input data.
        :return: The tree's final evaluated value.
        """
        # If we're just an int wrapper, return the int.
        if not isinstance(self._expression, tuple):
            return self._expression

        if type(input_vector) is str:
            input_vector = tuple(float(x) for x in input_vector.strip().split())

        fun_key, *params = self._expression
        evaluated_params = (param.evaluate(input_vector) for param in params)

        if fun_key in MATH_FUNCTIONS:
            fun = MATH_FUNCTIONS[fun_key].fun
            return fun(*evaluated_params)

        elif fun_key in DATA_FUNCTIONS:
            fun = DATA_FUNCTIONS[fun_key].fun
            return fun(*evaluated_params, input_vector)

        raise ValueError("Invalid function: ", fun_key)

    def simplify(self):

        # If we're just an int wrapper, we're as simple as can be!
        if type(self._expression) is not tuple:
            new_expression = self._expression

        # If we're wrapping an expression, evaluate as much as possible.
        else:
            fun_key, *params = self._expression
            simplified_params = [param.simplify() for param in params]
            param_expressions = [p._expression for p in simplified_params]

            # If all our parameters are numbers, we can do maths!
            if fun_key in MATH_FUNCTIONS and all(type(exp) is not tuple for exp in param_expressions):
                fun = MATH_FUNCTIONS[fun_key].fun
                new_expression = fun(*param_expressions)

            # If only some of our parameters are numbers, we can still do maths!
            else:
                new_expression = lazy_evaluate(fun_key, simplified_params)

        if type(new_expression) is Tree:
            return new_expression

        return Tree(new_expression)

    def __le__(self, other):
        if type(self._expression) is tuple:
            raise TypeError("Cannot compare unevaluated expressions")
        return self._expression <= other

    def __ge__(self, other):
        if type(self._expression) is tuple:
            raise TypeError("Cannot compare unevaluated expressions")
        return self._expression >= other

    def _calculate_length(self):
        """
        Calculate the number of nodes in this tree.
        :return: The number of nodes in the tree.
        """
        if type(self._expression) is tuple:
            return 1 + sum(len(param) for param in self._expression[1:])
        return 1

    def _calculate_string(self):
        """
        Display a tree like ["mul", 2, 3] as (mul 2 3).
        :return: A formatted string representation of this tree.
        """
        if type(self._expression) is tuple:
            return f"({self._expression[0]} {' '.join(map(str, self._expression[1:]))})"
        return str(self._expression)

    def _calculate_height(self):
        """
        Calculate the maximum height of a tree.
        :return: The length of the longest path from root to leaf.
        """
        if type(self._expression) == tuple:
            return 1 + max(x.height for x in self._expression[1:])
        return 0

    def __len__(self):
        return self._length

    def __str__(self):
        return self._string

    __repr__ = __str__

    def __eq__(self, other):
        if type(self._expression) is tuple:
            return str(self) == str(other)
        return self._expression == other

    def replace_subtree_at(self, index, new_subtree):
        """
        Replace a node with a new subtree.
        :param index: The index of the node to replace.
        :param new_subtree: The new node to replace it with.
        :return: A tree with the solution replaced.
        """

        # Check the index is actually in this tree.
        if index >= self._length:
            raise IndexError(f"Index out of bounds: {index} (max {self._length - 1})")

        # If we're replacing the whole tree, do it here.
        if index == 0:
            return new_subtree

        # Count the current node.
        index -= 1

        # Build a new expression list, recursively replacing the subtree once.
        new_expression_list = [self._expression[0]]
        found = False
        for subtree in self._expression[1:]:
            if not found and index < len(subtree):
                found = True
                subtree = subtree.replace_subtree_at(index, new_subtree)
            else:
                index -= len(subtree)
            new_expression_list.append(subtree)

        return Tree(new_expression_list)

    def subtree_at(self, index, _depth=0):
        """
        Return the subtree (and depth of that subtree) at an index.
        The index refers to a depth-first search of the subtree.
        :param index: The index of the node to find.
        :param _depth: The depth of the current node.
        :return: A tuple of (depth of node, node at index).
        """

        # Check the index is actually in this tree.
        if index >= self._length:
            raise IndexError(f"Index out of bounds: {index} (max {self._length - 1})")

        # An index of 0 means the root node.
        if index == 0:
            return _depth, self

        # Count the current node.
        index -= 1

        # Look for the tree that the index will be in.
        for tree in self._expression[1:]:
            if index < len(tree):
                depth, subtree = tree.subtree_at(index, _depth + 1)
                break
            else:
                index -= len(tree)
        else:
            raise IndexError("Got to the end without finding it!")

        return depth, subtree