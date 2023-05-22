import pytest
from penman.exceptions import ModelError
from penman.model import Model
from penman.graph import Graph


def test_deinvert(self, mini_amr):
    m = Model()
    assert (m.deinvert(('a', ':ARG0', 'b')) == ('a', ':ARG0', 'b'))
    assert (m.deinvert(('a', ':ARG0-of', 'b')) == ('b', ':ARG0', 'a'))
    assert (m.deinvert(('a', ':consist-of', 'b')) == ('b', ':consist', 'a'))
    assert (m.deinvert(('a', ':mod', 'b')) == ('a', ':mod', 'b'))
    assert (m.deinvert(('a', ':domain', 'b')) == ('a', ':domain', 'b'))
    m = Model.from_dict(mini_amr)
    assert (m.deinvert(('a', ':ARG0', 'b')) == ('a', ':ARG0', 'b'))
    assert (m.deinvert(('a', ':ARG0-of', 'b')) == ('b', ':ARG0', 'a'))
    assert (m.deinvert(('a', ':consist-of', 'b')) == ('a', ':consist-of', 'b'))
    assert (m.deinvert(('a', ':mod', 'b')) == ('a', ':mod', 'b'))
    assert (m.deinvert(('a', ':domain', 'b')) == ('a', ':domain', 'b'))
