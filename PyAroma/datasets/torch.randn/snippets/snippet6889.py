import pytest
import numpy as np
import torch
import torch_testing as tt
from rlil.environments.state import State


def test_custom_constructor_args():
    raw = torch.randn(3, 4)
    mask = torch.zeros(3).bool()
    info = ['a', 'b', 'c']
    state = State(raw, mask=mask, info=info)
    tt.assert_equal(state.features, raw)
    tt.assert_equal(state.mask, torch.zeros(3, dtype=torch.bool))
    assert (state.info == info)
