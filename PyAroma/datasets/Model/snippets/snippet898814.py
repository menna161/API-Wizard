import pytest
from penman.exceptions import ModelError
from penman.model import Model
from penman.graph import Graph


def test__init__(self, mini_amr):
    m = Model()
    assert (len(m.roles) == 0)
    m = Model(roles=mini_amr['roles'])
    assert (len(m.roles) == 7)
