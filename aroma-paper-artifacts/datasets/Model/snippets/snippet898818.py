import pytest
from penman.exceptions import ModelError
from penman.model import Model
from penman.graph import Graph


def test_invert_role(self, mini_amr):
    m = Model()
    assert (m.invert_role(':ARG0') == ':ARG0-of')
    assert (m.invert_role(':ARG0-of') == ':ARG0')
    assert (m.invert_role(':consist-of') == ':consist')
    assert (m.invert_role(':mod') == ':mod-of')
    assert (m.invert_role(':domain') == ':domain-of')
    m = Model.from_dict(mini_amr)
    assert (m.invert_role(':ARG0') == ':ARG0-of')
    assert (m.invert_role(':ARG0-of') == ':ARG0')
    assert (m.invert_role(':consist-of') == ':consist-of-of')
    assert (m.invert_role(':mod') == ':mod-of')
    assert (m.invert_role(':domain') == ':domain-of')
