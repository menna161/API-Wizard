import pytest
import numpy as np
import torch
import torch_testing as tt
from rlil.environments.state import State


def test_done():
    raw = torch.randn(1, 4)
    state = State(raw, mask=DONE)
    assert state.done
