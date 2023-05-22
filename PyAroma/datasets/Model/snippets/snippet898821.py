import pytest
from penman.exceptions import ModelError
from penman.model import Model
from penman.graph import Graph


def test_canonicalize_role(self, mini_amr):
    m = Model()
    assert (m.canonicalize_role(':ARG0') == ':ARG0')
    assert (m.canonicalize_role(':ARG0-of') == ':ARG0-of')
    assert (m.canonicalize_role(':ARG0-of-of') == ':ARG0')
    assert (m.canonicalize_role(':consist') == ':consist')
    assert (m.canonicalize_role(':consist-of') == ':consist-of')
    assert (m.canonicalize_role(':consist-of-of') == ':consist')
    assert (m.canonicalize_role(':mod') == ':mod')
    assert (m.canonicalize_role(':mod-of') == ':mod-of')
    assert (m.canonicalize_role(':domain') == ':domain')
    assert (m.canonicalize_role(':domain-of') == ':domain-of')
    assert (m.canonicalize_role('ARG0') == ':ARG0')
    assert (m.canonicalize_role('ARG0-of') == ':ARG0-of')
    assert (m.canonicalize_role('ARG0-of-of') == ':ARG0')
    m = Model.from_dict(mini_amr)
    assert (m.canonicalize_role(':ARG0') == ':ARG0')
    assert (m.canonicalize_role(':ARG0-of') == ':ARG0-of')
    assert (m.canonicalize_role(':ARG0-of-of') == ':ARG0')
    assert (m.canonicalize_role(':consist') == ':consist-of-of')
    assert (m.canonicalize_role(':consist-of') == ':consist-of')
    assert (m.canonicalize_role(':consist-of-of') == ':consist-of-of')
    assert (m.canonicalize_role(':mod') == ':mod')
    assert (m.canonicalize_role(':mod-of') == ':domain')
    assert (m.canonicalize_role(':domain') == ':domain')
    assert (m.canonicalize_role(':domain-of') == ':mod')
    assert (m.canonicalize_role('consist') == ':consist-of-of')
    assert (m.canonicalize_role('consist-of') == ':consist-of')
    assert (m.canonicalize_role('consist-of-of') == ':consist-of-of')
