import pytest
from penman.exceptions import ModelError
from penman.model import Model
from penman.graph import Graph


def test_reify(self, mini_amr):
    m = Model()
    with pytest.raises(ModelError):
        m.reify(('a', ':ARG0', 'b'))
    with pytest.raises(ModelError):
        m.reify(('a', ':accompanier', 'b'))
    with pytest.raises(ModelError):
        m.reify(('a', ':domain', 'b'))
    with pytest.raises(ModelError):
        m.reify(('a', ':mod', 'b'))
    m = Model.from_dict(mini_amr)
    with pytest.raises(ModelError):
        m.reify(('a', ':ARG0', 'b'))
    assert (m.reify(('a', ':accompanier', 'b')) == (('_', ':ARG0', 'a'), ('_', ':instance', 'accompany-01'), ('_', ':ARG1', 'b')))
    with pytest.raises(ModelError):
        assert m.reify(('a', ':domain', 'b'))
    assert (m.reify(('a', ':mod', 'b')) == (('_', ':ARG1', 'a'), ('_', ':instance', 'have-mod-91'), ('_', ':ARG2', 'b')))
    assert (m.reify(('a', ':mod', 'b'), variables={'a', 'b', '_'}) == (('_2', ':ARG1', 'a'), ('_2', ':instance', 'have-mod-91'), ('_2', ':ARG2', 'b')))
