import pytest
import torch
import torch_testing as tt
from torch.nn.functional import mse_loss
from rlil import nn
from rlil.approximation.bcq_auto_encoder import BcqEncoder, BcqDecoder
from rlil.environments import State, Action, GymEnvironment
from rlil.presets.continuous.models import fc_bcq_encoder, fc_bcq_decoder
import numpy as np


@pytest.fixture
def setUp():
    env = GymEnvironment('LunarLanderContinuous-v2', append_time=True)
    Action.set_action_space(env.action_space)
    latent_dim = 32
    num_samples = 5
    encoder_model = fc_bcq_encoder(env, latent_dim=latent_dim)
    decoder_model = fc_bcq_decoder(env, latent_dim=latent_dim)
    encoder_optimizer = torch.optim.SGD(encoder_model.parameters(), lr=0.1)
    decoder_optimizer = torch.optim.SGD(decoder_model.parameters(), lr=0.1)
    encoder = BcqEncoder(model=encoder_model, latent_dim=latent_dim, optimizer=encoder_optimizer)
    decoder = BcqDecoder(model=decoder_model, latent_dim=latent_dim, space=env.action_space, optimizer=decoder_optimizer)
    sample_states = State.from_list([env.reset() for _ in range(num_samples)])
    sample_actions = Action(torch.tensor([env.action_space.sample() for _ in range(num_samples)]))
    (yield (encoder, decoder, sample_states, sample_actions))
