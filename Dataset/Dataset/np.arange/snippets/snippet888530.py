import numpy as np
import pytest
import whynot as wn
from whynot.framework import parameter
from whynot.framework import ExperimentParameter


@parameter(name='a', default=1)
@parameter(name='b', default=3, values=[3, 4])
@parameter(name='c', default=4, values=np.arange(0.05, 0.95, 0.1))
def values_test(a, b, c):
    return ((a + b) + c)
