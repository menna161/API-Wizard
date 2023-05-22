from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import random
from absl.testing import absltest
from absl.testing import parameterized
from mathematics_dataset.sample import linear_system
from six.moves import range
import sympy


@parameterized.parameters([1, 2, 3])
def testLinearSystem(self, degree):
    for _ in range(100):
        target = [random.randint((- 100), 100) for _ in range(degree)]
        variables = [sympy.Symbol(chr((ord('a') + i))) for i in range(degree)]
        system = linear_system.linear_system(variables=variables, solutions=target, entropy=10.0)
        solved = sympy.solve(system, variables)
        solved = [solved[symbol] for symbol in variables]
        self.assertEqual(target, solved)
