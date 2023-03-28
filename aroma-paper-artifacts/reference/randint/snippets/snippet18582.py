import afnumpy
import numpy
import afnumpy as af
import numpy as np
from asserts import *
import pytest


def test_ndarray_all():
    b = numpy.random.randint(0, 2, 3).astype('bool')
    a = afnumpy.array(b)
    iassert(a.all(), b.all())
    iassert(a.all(axis=0), b.all(axis=0))
    b = numpy.random.randint(0, 2, (3, 2)).astype('bool')
    a = afnumpy.array(b)
    iassert(a.all(), b.all())
    iassert(a.all(axis=0), b.all(axis=0))
    iassert(a.all(keepdims=True), b.all(keepdims=True))
