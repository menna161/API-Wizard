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


def testCoefficientsLinearSplit(self):
    for degree in range(3):
        for ndims in range(3):
            for _ in range(10):
                coefficients = np.random.randint((- 5), 5, ([(degree + 1)] * ndims))
                entropy = random.uniform(1, 4)
                (c1, c2, coeffs1, coeffs2) = polynomials.coefficients_linear_split(coefficients, entropy)
                c1 = int(c1)
                c2 = int(c2)
                coeffs1 = np.asarray(coeffs1, dtype=np.int32)
                coeffs2 = np.asarray(coeffs2, dtype=np.int32)
                sum_ = ((c1 * coeffs1) + (c2 * coeffs2))
                self.assertAllEqual(sum_, coefficients)
