import chainer
from chainer_compiler.elichika import testtools
import numpy as np
from itertools import product


def main():
    testtools.generate_testcase(SimpleList(), [], subname='simple_list')
    testtools.generate_testcase(ListIterate(), [], subname='list_iterate')
    testtools.generate_testcase(ListInConstructor(), [], subname='list_in_constructor')
    testtools.generate_testcase(ListSubscript, [], subname='list_subscript')
    testtools.generate_testcase(IfListSubscriptAssign, [], subname='if_list_subscript_assign')
    testtools.generate_testcase(ArraySubscript, [], subname='array_subscript')
    (x, y) = (np.arange((((2 * 3) * 4) * 5)).reshape((2, 3, 4, 5)) for _ in range(2))
    testtools.generate_testcase(ArraySubscriptFancy, [x, y], subname='array_subscript_fancy')
    tensor = np.array([1, 2, 3, 4, 5])
    testtools.generate_testcase(TensorToList(), [tensor], subname='tensor_to_list')
