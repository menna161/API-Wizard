import afnumpy
import numpy
import afnumpy as af
import numpy as np
from asserts import *
import pytest


def test_unary_operators():
    a = afnumpy.random.rand(3)
    b = numpy.array(a)
    fassert((- a), (- b))
    fassert((+ a), (+ b))
    b = numpy.random.randint(0, 2, 3).astype('bool')
    a = afnumpy.array(b)
    fassert((- a), (~ b))
    fassert((+ a), (+ b))
