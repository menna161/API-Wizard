import os
import numpy as np
import pytest
from airfoils import Airfoil
import airfoils.__version__ as v


def test_camber_line_angle(airfoil):
    "\n    Test 'camber_line_angle' method\n    "
    for xsi in np.linspace(0, 1, num=50):
        assert (airfoil.camber_line_angle(xsi) == 0)
