import pytest
import torch
import torch_testing as tt
from torch.nn.functional import mse_loss
from rlil import nn
from rlil.approximation.bcq_auto_encoder import BcqEncoder, BcqDecoder
from rlil.environments import State, Action, GymEnvironment
from rlil.presets.continuous.models import fc_bcq_encoder, fc_bcq_decoder
import numpy as np


def test_reinforce(setUp):
    (encoder, decoder, states, actions) = setUp
    (mean, log_var) = encoder(states, actions)
    z = (mean + ((0.5 * log_var).exp() * torch.randn_like(log_var)))
    dec = decoder(states, z)
    loss = mse_loss(actions.features, dec)
    for _ in range(100):
        (mean, log_var) = encoder(states, actions)
        z = (mean + (log_var.exp() * torch.randn_like(log_var)))
        dec = decoder(states, z)
        new_loss = mse_loss(actions.features, dec)
        decoder.reinforce(new_loss)
        encoder.reinforce()
    assert (new_loss < loss)
    z = (mean + ((0.5 * log_var).exp() * torch.randn_like(log_var)))
    dec = decoder(states, z)
    loss = nn.kl_loss_vae(mean, log_var)
    for _ in range(10):
        (mean, log_var) = encoder(states, actions)
        z = (mean + (log_var.exp() * torch.randn_like(log_var)))
        dec = decoder(states, z)
        new_loss = nn.kl_loss_vae(mean, log_var)
        decoder.reinforce(new_loss)
        encoder.reinforce()
    assert (new_loss < loss)
