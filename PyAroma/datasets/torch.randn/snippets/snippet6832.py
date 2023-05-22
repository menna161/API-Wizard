import pytest
import torch
import torch_testing as tt
from torch.nn.functional import mse_loss
from rlil import nn
from rlil.approximation.bcq_auto_encoder import BcqEncoder, BcqDecoder
from rlil.environments import State, Action, GymEnvironment
from rlil.presets.continuous.models import fc_bcq_encoder, fc_bcq_decoder
import numpy as np


def test_decode(setUp):
    (encoder, decoder, states, actions) = setUp
    (mean, log_var) = encoder(states, actions)
    z = (mean + ((0.5 * log_var).exp() * torch.randn_like(log_var)))
    dec = decoder(states, z)
    assert (actions.shape == dec.shape)
