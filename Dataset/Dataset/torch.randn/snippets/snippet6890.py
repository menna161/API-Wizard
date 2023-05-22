import pytest
import numpy as np
import torch
import torch_testing as tt
from rlil.environments.state import State


def test_not_done():
    state = State(torch.randn(1, 4))
    assert (not state.done)
