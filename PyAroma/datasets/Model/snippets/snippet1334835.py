import numpy as np
import pytest
from astropy.modeling.core import Model, Fittable1DModel, InputParameterError
from astropy.modeling.parameters import Parameter, ParameterDefinitionError
from astropy.modeling.models import Gaussian1D, Pix2Sky_TAN, RotateNative2Celestial, Rotation2D
from astropy import units as u
from astropy.units import UnitsError
from astropy.tests.helper import assert_quantity_allclose
from astropy import coordinates as coord


@pytest.mark.parametrize(('unit', 'default'), ((u.m, 1.0), (None, (1 * u.m))))
def test_parameter_defaults(unit, default):
    '\n    Test that default quantities are correctly taken into account\n    '

    class TestModel(BaseTestModel):
        a = Parameter(default=default, unit=unit)
    assert (TestModel.a.unit == u.m)
    assert (TestModel.a.default == 1.0)
    m = TestModel()
    assert (m.a.unit == u.m)
    assert (m.a.default == m.a.value == 1.0)
    m = TestModel((2.0 * u.m))
    assert (m.a.unit == u.m)
    assert (m.a.value == 2.0)
    assert (m.a.default == 1.0)
    m = TestModel((2.0 * u.pc))
    assert (m.a.unit == u.pc)
    assert (m.a.value == 2.0)
    assert (m.a.default == 1.0)
    m = TestModel((2.0 * u.Jy))
    assert (m.a.unit == u.Jy)
    assert (m.a.value == 2.0)
    assert (m.a.default == 1.0)
    with pytest.raises(InputParameterError) as exc:
        TestModel(1.0)
    assert (exc.value.args[0] == "TestModel.__init__() requires a Quantity for parameter 'a'")
