import argparse
#from util import *

#args = parser.parse_args()

#input_expression = args.expression
#dimension = args.dimension
#input_vector = args.vector
import argparse
import queue
import time
from threading import Thread

from evaluate_fitness import evaluate_fitness_against_data
from genetic_algorithm import genetic_algorithm
from solution import Solution
from tree import Tree


def q1(expr, x):
    result = Tree(expr).evaluate(x)
    print(result)
    return result


def q2(expr, data):
    print(Solution(expr).evaluate_fitness_against(data))


def q3(m, data, time_budget, lambda_):
    start = time.perf_counter()

    # Perform the genetic algorithm.
    results_queue = queue.LifoQueue()
    computation_thread = Thread(
        target=lambda: genetic_algorithm(lambda_, m, 2**100, training=data, results_queue=results_queue),
        daemon=True  # Allow exiting when the timer runs out.
    )
    computation_thread.start()

    # Wait max. of time-budget seconds for the algorithm to finish.

    time.sleep(time_budget-(time.perf_counter() - start - 0.1))
    best = results_queue.get_nowait()
    print(best.tree)


def main(args):
    expr = args.expr
    if expr and "(" not in expr:
        expr = f"({expr})"

    if args.question == 1:
        q1(expr, args.x)

    elif args.question == 2:
        q2(expr, args.data)

    elif args.question == 3:
        q3(args.m, args.data, args.time_budget, args.lambda_)


if __name__ == "__main__":

    def arguments():
        parser = argparse.ArgumentParser(description='NISO') 
        # Instance file argument
        parser.add_argument('-n', type=int, help='Dimension of the input vector')
        # The input vector argument
        parser.add_argument('-x', type=str, help='The input vector')
        parser.add_argument('-m', type=int)
        parser.add_argument('-question', type=int)
        #expression
        parser.add_argument('-expr', type=str, help='Expression to evaluate')
        parser.add_argument('-data')
        parser.add_argument('-lambda', type=int, dest="lambda_")
        parser.add_argument('-time_budget', type=int)
        return parser.parse_args()
    main(arguments())