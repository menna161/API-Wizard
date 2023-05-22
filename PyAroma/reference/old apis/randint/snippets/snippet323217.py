import unittest
from random import randint, random
from ands.algorithms.dp.fibonacci import bottom_up_fibonacci, memoized_fibonacci, recursive_fibonacci


def test_fib_n(self):
    n = randint(3, 30)
    fib_n = recursive_fibonacci(n)
    self.assertEqual(fib_n, memoized_fibonacci(n))
    self.assertEqual(fib_n, bottom_up_fibonacci(n))
