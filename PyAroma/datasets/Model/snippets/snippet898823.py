import pytest
from penman.exceptions import ModelError
from penman.model import Model
from penman.graph import Graph


def test_is_role_reifiable(self, mini_amr):
    m = Model()
    assert (not m.is_role_reifiable(':ARG0'))
    assert (not m.is_role_reifiable(':accompanier'))
    assert (not m.is_role_reifiable(':domain'))
    assert (not m.is_role_reifiable(':mod'))
    m = Model.from_dict(mini_amr)
    assert (not m.is_role_reifiable(':ARG0'))
    assert m.is_role_reifiable(':accompanier')
    assert (not m.is_role_reifiable(':domain'))
    assert m.is_role_reifiable(':mod')
