import pytest
from penman.exceptions import ModelError
from penman.model import Model
from penman.graph import Graph


def test_from_dict(self, mini_amr):
    assert (Model.from_dict(mini_amr) == Model(roles=mini_amr['roles'], normalizations=mini_amr['normalizations'], reifications=mini_amr['reifications']))
