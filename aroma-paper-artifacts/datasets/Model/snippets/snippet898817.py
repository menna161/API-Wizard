import pytest
from penman.exceptions import ModelError
from penman.model import Model
from penman.graph import Graph


def test_is_role_inverted(self, mini_amr):
    m = Model()
    assert m.is_role_inverted(':ARG0-of')
    assert m.is_role_inverted(':-of')
    assert (not m.is_role_inverted(':ARG0'))
    assert (not m.is_role_inverted(':'))
    assert m.is_role_inverted(':consist-of')
    m = Model.from_dict(mini_amr)
    assert m.is_role_inverted(':mod-of')
    assert m.is_role_inverted(':domain-of')
    assert (not m.is_role_inverted(':mod'))
    assert (not m.is_role_inverted(':domain'))
    assert m.is_role_inverted(':consist-of-of')
    assert (not m.is_role_inverted(':consist-of'))
