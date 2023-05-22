import numpy as np
import pytest
import whynot as wn
from whynot.framework import parameter
from whynot.framework import ExperimentParameter


def test_parameter():
    'Test the parameter decorator.'

    @parameter(name='a', default=1, values=[1, 2], description='test a')
    @parameter(name='b', default=3, values=[3, 4], description='test b')
    def foo(a, b):
        return (a + b)

    def check_params(listed, returned):
        assert (set(listed) == set((p.name for p in returned)))
    check_params(['a', 'b'], wn.framework.extract_params(foo, standard_args=[]))

    @parameter(name='b', default=3, values=[3, 4], description='test b')
    def bar(a, b):
        return (a + b)
    check_params(['b'], wn.framework.extract_params(bar, standard_args=['a']))
    with pytest.raises(ValueError):
        wn.framework.extract_params(bar, standard_args=[])
    with pytest.raises(ValueError):

        @parameter(name='a', default=0)
        def baz(propensity):
            return propensity
    with pytest.raises(ValueError):

        @parameter(name='rng', default=0)
        def foobar(rng):
            return 2
        wn.framework.extract_params(foobar, standard_args=['rng'])

    @parameter(name='a', default=1)
    @parameter(name='b', default=3, values=[3, 4])
    @parameter(name='c', default=4, values=np.arange(0.05, 0.95, 0.1))
    def values_test(a, b, c):
        return ((a + b) + c)
    param_collection = wn.framework.extract_params(values_test, standard_args=[])
    sampled = param_collection.sample()
    assert (sampled['a'] == 1)
    print(sampled)
