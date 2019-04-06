from math import floor
from statistics import mean
from safety_harness import safety_harness
from function import Function

def index(param, input_vector):
    return floor(abs(param)) % (len(input_vector))


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
    "data": Function(data, 1),
    "diff": Function(diff, 2),
    "avg": Function(avg, 2)
}

for key, function in DATA_FUNCTIONS.items():
    DATA_FUNCTIONS[key] = safety_harness(function)