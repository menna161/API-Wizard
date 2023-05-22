import pytest
from penman.exceptions import ModelError
from penman.model import Model
from penman.graph import Graph


def test_invert(self, mini_amr):
    m = Model()
    assert (m.invert(('a', ':ARG0', 'b')) == ('b', ':ARG0-of', 'a'))
    assert (m.invert(('a', ':ARG0-of', 'b')) == ('b', ':ARG0', 'a'))
    assert (m.invert(('a', ':consist-of', 'b')) == ('b', ':consist', 'a'))
    assert (m.invert(('a', ':mod', 'b')) == ('b', ':mod-of', 'a'))
    assert (m.invert(('a', ':domain', 'b')) == ('b', ':domain-of', 'a'))
    m = Model.from_dict(mini_amr)
    assert (m.invert(('a', ':ARG0', 'b')) == ('b', ':ARG0-of', 'a'))
    assert (m.invert(('a', ':ARG0-of', 'b')) == ('b', ':ARG0', 'a'))
    assert (m.invert(('a', ':consist-of', 'b')) == ('b', ':consist-of-of', 'a'))
    assert (m.invert(('a', ':mod', 'b')) == ('b', ':mod-of', 'a'))
    assert (m.invert(('a', ':domain', 'b')) == ('b', ':domain-of', 'a'))
