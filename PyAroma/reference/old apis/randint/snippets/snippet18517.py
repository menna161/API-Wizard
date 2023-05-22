import afnumpy
import afnumpy as af
import numpy
import numpy as np
from asserts import *
import pytest


def test_isnan():
    b = (1.0 * numpy.random.randint(0, 2, (2, 3)))
    b[(b == 0)] = numpy.nan
    a = afnumpy.array(b)
    fassert(afnumpy.isnan(a), numpy.isnan(b))
