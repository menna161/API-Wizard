import pytest
import numpy as np
import torch
import torch_testing as tt
from rlil.environments.state import State


def test_constructor_defaults():
    raw = torch.randn(3, 4)
    state = State(raw)
    tt.assert_equal(state.features, raw)
    tt.assert_equal(state.mask, torch.ones(3, dtype=torch.bool))
    tt.assert_equal(state.raw, raw)
    assert (state.info == ([None] * 3))
