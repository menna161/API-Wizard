import math
import unittest
from random import randint
from ands.algorithms.recursion.factorial import *


def test_factorial_random_number(self):
    r = randint(2, 100)
    self.assertEqual(factorial(r), math.factorial(r))
    self.assertEqual(iterative_factorial(r), math.factorial(r))
