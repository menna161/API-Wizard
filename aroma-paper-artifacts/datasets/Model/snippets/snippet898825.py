import pytest
from penman.exceptions import ModelError
from penman.model import Model
from penman.graph import Graph


def test_is_concept_dereifiable(self, mini_amr):
    m = Model()
    assert (not m.is_concept_dereifiable('chase-01'))
    assert (not m.is_concept_dereifiable(':mod'))
    assert (not m.is_concept_dereifiable('have-mod-91'))
    m = Model.from_dict(mini_amr)
    assert (not m.is_concept_dereifiable('chase-01'))
    assert (not m.is_concept_dereifiable(':mod'))
    assert m.is_concept_dereifiable('have-mod-91')
