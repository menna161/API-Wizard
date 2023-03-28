import unittest
from random import randint, uniform
from numpy.polynomial.polynomial import polyval
from ands.algorithms.numerical.horner import horner


def setUp(self):
    self.x0 = uniform((- 10.0), (- 10.0))
    self.degree = randint(0, 30)
    self.coefficients = [uniform((- 10), 10) for _ in range((self.degree + 1))]
