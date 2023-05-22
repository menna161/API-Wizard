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


def testExpandCoefficients(self):
    for _ in range(10):
        num_variables = np.random.randint(1, 4)
        degrees = np.random.randint(0, 4, [num_variables])
        coefficients = np.random.randint((- 3), 3, (degrees + 1))
        entropy = np.random.uniform(0, 10)
        expanded = polynomials.expand_coefficients(coefficients, entropy)
        collapsed = np.vectorize(sum)(expanded)
        self.assertAllEqual(coefficients, collapsed)
