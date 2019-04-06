import random
from random import randrange

from evaluate_fitness import evaluate_fitness_against_data

from tree import Tree


LENGTH_PENALTY = 0.0


class Solution:
    def __init__(self, expression_tree):
        if type(expression_tree) is str:
            expression_tree = Tree(expression_tree)
        self.expression_tree = expression_tree
        self.fitness = None
        self.length = len(self.expression_tree)

    def __str__(self):
        return f"Solution(fitness={self.fitness}, tree={self.expression_tree})"

    @property
    def tree(self):
        return self.expression_tree

    def evaluate(self, input_vector):
        return self.expression_tree.evaluate(input_vector)

    def evaluate_fitness_against(self, training_data):
        self.fitness = evaluate_fitness_against_data(self.expression_tree, training_data)
        return self.fitness

    def mutate(self, p_select_subtree=0.5):
        """
        Return a mutated version of this solution.
        :return: A mutated solution.
        """

        # Prevent circular imports.
        from generation import create_random_node, MAX_DEPTH

        # Pick a random node and get its depth.
        random_index = randrange(len(self.expression_tree))
        node_depth, subtree = self.expression_tree.subtree_at(random_index)

        # With some probability, just return that random node.
        if random.random() < p_select_subtree:
            return Solution(subtree)

        # Otherwise, create a random node with an appropriate max-depth.
        max_possible_depth = MAX_DEPTH - node_depth

        # Mutate until the node has actually changed. (Randomness sometimes repeats!)
        while True:
            random_tree = create_random_node(max_depth=max_possible_depth)
            if random_tree != subtree:
                break

        # Replace initial node with the one we've created in a new tree
        new_tree = self.expression_tree.replace_subtree_at(random_index, random_tree)

        # Create & return a Solution with that tree
        return Solution(new_tree)

    def crossover(self, other):
        random_index = randrange(min(len(self.expression_tree), len(other.expression_tree)))
        _, subtree_one = self.expression_tree.subtree_at(random_index)
        _, subtree_two = other.expression_tree.subtree_at(random_index)
        tree_one = self.expression_tree.replace_subtree_at(random_index, subtree_two)
        tree_two = other.expression_tree.replace_subtree_at(random_index, subtree_one)
        return Solution(tree_one), Solution(tree_two)

    def simplify(self):
        new_solution = Solution(self.expression_tree.simplify())
        new_solution.fitness = self.fitness
        return new_solution