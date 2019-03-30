from math import floor
from statistics import mean
from safety_harness import safety_harness


def index(param, input_vector):
    return floor(abs(param)) % (len(input_vector) + 1)


def data(param, input_vector):
    return input_vector[index(param, input_vector)]


def diff(param1, param2, input_vector=None):
    data1 = data(param1, input_vector)
    data2 = data(param2, input_vector)
    return data1 - data2


def avg(param1, param2, input_vector=None):
    i1 = index(param1, input_vector)
    i2 = index(param2, input_vector)
    i1, i2 = sorted((i1, i2))
    return mean(input_vector[i1:i2])


DATA_FUNCTIONS = {
    "data": data,
    "diff": diff,
    "avg": avg
}

for key, function in DATA_FUNCTIONS.items():
    DATA_FUNCTIONS[key] = safety_harness(function)