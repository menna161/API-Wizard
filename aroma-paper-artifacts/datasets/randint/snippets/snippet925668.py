from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import random
from absl.testing import absltest
from absl.testing import parameterized
from mathematics_dataset.sample import arithmetic
from mathematics_dataset.sample import number
from mathematics_dataset.sample import ops
from six.moves import range
import sympy


def testArithmeticLength(self):
    'Tests that the generated arithmetic expressions have given length.'
    for _ in range(1000):
        target = number.integer_or_rational(4, signed=True)
        entropy = 8.0
        length = random.randint(2, 10)
        expression = arithmetic.arithmetic(target, entropy, length)
        actual_length = (len(ops.number_constants(expression)) - 1)
        self.assertEqual(actual_length, length)
