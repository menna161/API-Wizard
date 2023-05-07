import os
import sys
import subprocess
import pytest
import numpy as np
from inspect import signature
from numpy.testing import assert_allclose
import astropy
from astropy.modeling.core import Model, custom_model
from astropy.modeling.parameters import Parameter
from astropy.modeling import models
import astropy.units as u
from astropy.tests.helper import assert_quantity_allclose
import scipy


def test_Model_instance_repr_and_str():
    m = NonFittableModel(42.5)
    assert (repr(m) == '<NonFittableModel(a=42.5)>')
    assert (str(m) == 'Model: NonFittableModel\nInputs: ()\nOutputs: ()\nModel set size: 1\nParameters:\n     a  \n    ----\n    42.5')
    assert (len(m) == 1)