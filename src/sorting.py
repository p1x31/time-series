import random


def stochastic_sort(population, number_sweeps, wrong_choice):
    """
    A simplified version of stochastic sort, where no penalties are enacted,
    but we make the wrong choice about whether to swap indices i and i+1
    with some probability. We scale the number of sweeps linearly with the
    size of the input.
    :param population: Ordered sequence of population.
    :param number_sweeps: Number of iterations through the pseudo-bubble-sort algorithm.
    :param wrong_choice: Probability of choosing incorrectly whether to swap.
    :return: The population after applying stochastic-sort.
    """
    population = [p for p in population]
    random.shuffle(population)  # Don't maintain any preexisting order.
    number_sweeps = int(number_sweeps * len(population))

    def swap(i, j):
        population[i], population[j] = population[j], population[i]

    def fitness(i):
        # Here, we're trying to *minimise* cost.
        return population[i].fitness

    for _ in range(number_sweeps):
        for i in range(len(population) - 1):
            should_swap = fitness(i) > fitness(i + 1)
            wrong_way = random.random() < wrong_choice
            if should_swap ^ wrong_way:
                swap(i, i+1)

    return population