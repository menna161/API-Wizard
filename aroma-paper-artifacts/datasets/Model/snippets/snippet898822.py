import pytest
from penman.exceptions import ModelError
from penman.model import Model
from penman.graph import Graph


def test_canonicalize(self, mini_amr):
    m = Model()
    assert (m.canonicalize(('a', ':ARG0', 'b')) == ('a', ':ARG0', 'b'))
    assert (m.canonicalize(('a', ':ARG0-of', 'b')) == ('a', ':ARG0-of', 'b'))
    assert (m.canonicalize(('a', ':ARG0-of-of', 'b')) == ('a', ':ARG0', 'b'))
    assert (m.canonicalize(('a', ':consist', 'b')) == ('a', ':consist', 'b'))
    assert (m.canonicalize(('a', ':consist-of', 'b')) == ('a', ':consist-of', 'b'))
    assert (m.canonicalize(('a', ':consist-of-of', 'b')) == ('a', ':consist', 'b'))
    assert (m.canonicalize(('a', ':mod', 'b')) == ('a', ':mod', 'b'))
    assert (m.canonicalize(('a', ':mod-of', 'b')) == ('a', ':mod-of', 'b'))
    assert (m.canonicalize(('a', ':domain', 'b')) == ('a', ':domain', 'b'))
    assert (m.canonicalize(('a', ':domain-of', 'b')) == ('a', ':domain-of', 'b'))
    assert (m.canonicalize(('a', 'ARG0', 'b')) == ('a', ':ARG0', 'b'))
    assert (m.canonicalize(('a', 'ARG0-of', 'b')) == ('a', ':ARG0-of', 'b'))
    assert (m.canonicalize(('a', 'ARG0-of-of', 'b')) == ('a', ':ARG0', 'b'))
    m = Model.from_dict(mini_amr)
    assert (m.canonicalize(('a', ':ARG0', 'b')) == ('a', ':ARG0', 'b'))
    assert (m.canonicalize(('a', ':ARG0-of', 'b')) == ('a', ':ARG0-of', 'b'))
    assert (m.canonicalize(('a', ':ARG0-of-of', 'b')) == ('a', ':ARG0', 'b'))
    assert (m.canonicalize(('a', ':consist', 'b')) == ('a', ':consist-of-of', 'b'))
    assert (m.canonicalize(('a', ':consist-of', 'b')) == ('a', ':consist-of', 'b'))
    assert (m.canonicalize(('a', ':consist-of-of', 'b')) == ('a', ':consist-of-of', 'b'))
    assert (m.canonicalize(('a', ':mod', 'b')) == ('a', ':mod', 'b'))
    assert (m.canonicalize(('a', ':mod-of', 'b')) == ('a', ':domain', 'b'))
    assert (m.canonicalize(('a', ':domain', 'b')) == ('a', ':domain', 'b'))
    assert (m.canonicalize(('a', ':domain-of', 'b')) == ('a', ':mod', 'b'))
    assert (m.canonicalize(('a', 'consist', 'b')) == ('a', ':consist-of-of', 'b'))
    assert (m.canonicalize(('a', 'consist-of', 'b')) == ('a', ':consist-of', 'b'))
    assert (m.canonicalize(('a', 'consist-of-of', 'b')) == ('a', ':consist-of-of', 'b'))
