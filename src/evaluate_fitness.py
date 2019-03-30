import csv
from statistics import mean
from collections import OrderedDict

from evaluate_expression import evaluate_expression


def mean_square_error(seq1, seq2):
    return mean((a - b) ** 2 for a, b in zip(seq1, seq2))


def evaluate_fitness_against_data(expression, training_data):
    calculated_results = (evaluate_expression(expression, input_vector) for input_vector in training_data)
    target_results = training_data.values()
    return mean_square_error(calculated_results, target_results)


def evaluate_fitness_against_file(expression, training_data_file):
    training_data = OrderedDict()

    with open(training_data_file) as f:
        for line in csv.reader(f, delimiter='\t'):
            *input_vector, output = line
            key = tuple(map(float, input_vector))
            training_data[key] = float(output)

    return evaluate_fitness_against_data(expression, training_data)