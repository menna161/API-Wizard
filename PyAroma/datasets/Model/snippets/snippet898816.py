import pytest
from penman.exceptions import ModelError
from penman.model import Model
from penman.graph import Graph


def test_has_role(self, mini_amr):
    m = Model()
    assert (not m.has_role(''))
    assert m.has_role(m.concept_role)
    assert (not m.has_role(':ARG0'))
    assert (not m.has_role(':ARG0-of'))
    m = Model.from_dict(mini_amr)
    assert (not m.has_role(''))
    assert m.has_role(m.concept_role)
    assert m.has_role(':ARG0')
    assert m.has_role(':ARG0-of')
    assert m.has_role(':mod')
    assert m.has_role(':mod-of')
    assert (not m.has_role(':consist'))
    assert m.has_role(':consist-of')
    assert m.has_role(':consist-of-of')
    assert (not m.has_role(':fake'))
    assert m.has_role(':op1')
    assert m.has_role(':op10')
    assert m.has_role(':op9999')
    assert (not m.has_role(':op[0-9]+'))
