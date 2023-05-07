import pytest
from penman.exceptions import ModelError
from penman.model import Model
from penman.graph import Graph


def test_dereify(self, mini_amr):
    t1 = ('_', ':instance', 'have-mod-91')
    t1b = ('_', ':instance', 'chase-01')
    t2 = ('_', ':ARG1', 'a')
    t3 = ('_', ':ARG2', 'b')
    m = Model()
    with pytest.raises(TypeError):
        m.dereify(t1)
    with pytest.raises(TypeError):
        m.dereify(t1, t2)
    with pytest.raises(ModelError):
        m.dereify(t1, t2, t3)
    m = Model.from_dict(mini_amr)
    assert (m.dereify(t1, t2, t3) == ('a', ':mod', 'b'))
    assert (m.dereify(t1, t3, t2) == ('a', ':mod', 'b'))
    with pytest.raises(ModelError):
        m.dereify(t1b, t2, t3)
