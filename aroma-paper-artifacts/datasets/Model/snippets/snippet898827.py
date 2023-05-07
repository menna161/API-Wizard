import pytest
from penman.exceptions import ModelError
from penman.model import Model
from penman.graph import Graph


def test_errors(self, mini_amr):
    m = Model()
    a = Model.from_dict(mini_amr)
    g = Graph([('a', ':instance', 'alpha')])
    assert (m.errors(g) == {})
    g = Graph([('a', ':instance', 'alpha'), ('a', ':mod', '1')])
    assert (m.errors(g) == {('a', ':mod', '1'): ['invalid role']})
    assert (a.errors(g) == {})
    g = Graph([('n', ':instance', 'name'), ('n', ':op1', 'Foo'), ('n', ':op2', 'Bar')])
    assert (a.errors(g) == {})
    g = Graph([('a', ':instance', 'alpha'), ('b', ':instance', 'beta')])
    assert (m.errors(g) == {('b', ':instance', 'beta'): ['unreachable']})
    assert (a.errors(g) == {('b', ':instance', 'beta'): ['unreachable']})
