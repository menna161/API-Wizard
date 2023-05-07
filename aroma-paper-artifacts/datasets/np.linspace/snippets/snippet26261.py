import os
import numpy as np
import pytest
from airfoils import Airfoil
import airfoils.__version__ as v


def test_camber_line(airfoil):
    "\n    Test 'camber_line' method\n    "
    for xsi in np.linspace(0, 1, num=50):
        assert (airfoil.camber_line(xsi) == 0)
