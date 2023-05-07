import random
import collections
import statistics
from hypothesis import given
import hypothesis.strategies as st
from hypothesis import find, settings, Verbosity
from hypothesis.strategies import lists, integers
import unittest
from strgen import StringGenerator as SG


def randint(self, a, b):
    return super().randint(a, b)
