import pytest
import numpy as np
import torch
import torch_testing as tt
from rlil.environments.state import State


def test_from_list():
    state1 = State(torch.randn(1, 4), mask=DONE, info=['a'])
    state2 = State(torch.randn(1, 4), mask=NOT_DONE, info=['b'])
    state3 = State(torch.randn(1, 4))
    state = State.from_list([state1, state2, state3])
    tt.assert_equal(state.raw, torch.cat((state1.raw, state2.raw, state3.raw)))
    tt.assert_equal(state.mask, torch.tensor([0, 1, 1]))
    assert (state.info == ['a', 'b', None])
