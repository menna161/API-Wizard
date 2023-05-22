import pytest
import numpy as np
import torch
import torch_testing as tt
from rlil.environments.state import State


def test_get_item():
    raw = torch.randn(3, 4)
    states = State(raw)
    state = states[2]
    tt.assert_equal(state.raw, raw[2].unsqueeze(0))
    tt.assert_equal(state.mask, NOT_DONE)
    assert (state.info == [None])
