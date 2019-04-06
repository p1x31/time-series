import random
import sys
from math import floor

from generation import generate_random_solutions
from sorting import stochastic_sort


def breed(parents, mutation_crossover_ratio, mutation_replacement_ratio):
    """
    Apply variation operators to all parents and generate the same
    number of children.
    :param parents: The parents to be bred.
    :param mutation_crossover_ratio: The probability that we'll mutate
        the next parent instead of using crossover.
    :param mutation_replacement_ratio: Described in mutate().
    :return: The children we've gained as a result of breeding.
    """
    children = []
    random.shuffle(parents)
    num_children = len(parents)

    while num_children:
        if num_children == 1 or random.random() < mutation_crossover_ratio:
            parent = parents[num_children-1]
            child = parent.mutate(mutation_replacement_ratio)
            children.append(child)
            num_children -= 1
        else:
            parent1, parent2 = parents[num_children-1], parents[num_children-2]
            child1, child2 = parent1.crossover(parent2)
            children.extend([child1, child2])
            num_children -= 2

    return children


def genetic_algorithm(pop_size=100, input_size=100, number_iterations=100, fraction_parents=0.3, p_simplify=0.01,
                      training=None, results_queue=None, stop_flag=None, mutation_crossover_ratio=0.2,
                      mutation_replacement_ratio=0.5, num_sweeps=3, wrong_choice=0.4):
    """
    Run an independent instance of the genetic algorithm.
    :param pop_size: The size of the population to evolve.
    :param input_size: The size of the input vectors in the training data.
    :param number_iterations: The number of generations of evolution.
    :param fraction_parents: Fraction of parents chosen from the population each generation
    :param training: The training data.
    :param p_simplify: The likelihood of simplifying a solution each generation.
    :param results_queue: A results queue to populate with the current best solution.
    :param stop_flag: When running in parallel, a flag to kill the thread.
    :param mutation_crossover_ratio: Described in the breed() function.
    :param mutation_replacement_ratio: Described in the mutate() method.
    :param num_sweeps: Described in stochastic_sort().
    :param wrong_choice: Described in stochastic_sort().
    :return: The population of the final generation.
    """

    if results_queue is None:
        raise ValueError("Results queue not present!")

    population = generate_random_solutions(pop_size, input_size, max_depth=5)
    num_children = num_parents = floor(pop_size * fraction_parents)
    for solution in population:
        solution.evaluate_fitness_against(training)
    best_so_far = population[0].simplify()

    results_queue.put(best_so_far)

    for i in range(number_iterations):

        # Check our stop-flag.
        if stop_flag:
            break

        population = stochastic_sort(population, num_sweeps, wrong_choice)

        # Simplify each expression with some probability each generation.
        population = [p.simplify() if random.random() < p_simplify else p for p in population]

        # Check for a new best-ever solution.
        for solution in population:
            better_fitness = solution.fitness < best_so_far.fitness
            same_fitness_simpler = solution.fitness == best_so_far.fitness and solution.length < best_so_far.length
            if better_fitness or same_fitness_simpler:
                best_so_far = solution.simplify()
        results_queue.put(best_so_far)

        # if stop_flag is not None:
        #     print(".", end='')
        #     sys.stdout.flush()

        # Pick parents and breed to get children.
        parents = population[:num_parents]
        children = breed(parents, mutation_crossover_ratio, mutation_replacement_ratio)
        for c in children:
            c.evaluate_fitness_against(training)

        # Replace lowest ranked individuals with children.
        population = children + population[:-num_children]

    return best_so_far