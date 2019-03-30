import argparse
from util import *

parser = argparse.ArgumentParser(description='NISO')

#expression
parser.add_argument('-expr', type=str, help='Expression to evaluate')
# Instance file argument
parser.add_argument('-n', type=str, help='Dimension of the input vector')

# The input vector argument
parser.add_argument('-x', type=str, help='The input vector')




args = parser.parse_args()

input_expression = args.expression
dimension = args.dimension
input_vector = args.vector
