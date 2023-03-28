import math
import unittest
from random import randint
from ands.algorithms.recursion.factorial import *


def test_multiple_factorial_random_n(self):
    ls = []
    r = randint(2, 10)
    for i in range((r + 1)):
        ls.append(math.factorial(i))
    self.assertEqual(multiple_factorial(r), ls)
