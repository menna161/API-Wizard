from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import random
from absl.testing import parameterized
from mathematics_dataset.sample import polynomials
import numpy as np
from six.moves import range
import sympy
import tensorflow as tf


def testSampleWithBrackets(self):
    (x, y) = sympy.symbols('x y')
    for _ in range(100):
        degrees = np.random.randint(1, 4, [2])
        entropy = random.uniform(0, 4)
        polynomial = polynomials.sample_with_brackets(variables=[x, y], degrees=degrees, entropy=entropy)
        self.assertIn('(', str(polynomial))
        poly = sympy.poly(sympy.sympify(polynomial).expand())
        self.assertEqual(poly.degree(x), degrees[0])
        self.assertEqual(poly.degree(y), degrees[1])
