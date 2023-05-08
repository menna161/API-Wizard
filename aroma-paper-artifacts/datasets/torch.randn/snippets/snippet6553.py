import torch
from torch.distributions.normal import Normal
from torch.nn.functional import mse_loss
from rlil.environments import State, action_decorator, Action
from rlil.initializer import get_device, get_writer, get_replay_buffer
from rlil import nn
from copy import deepcopy
from .base import Agent, LazyAgent
import os


def train(self):
    (states, actions, _, _, _, _) = self.replay_buffer.sample(self.minibatch_size)
    (mean, log_var) = self.encoder(states.to(self.device), actions.to(self.device))
    z = (mean + ((0.5 * log_var).exp() * torch.randn_like(log_var)))
    vae_actions = Action(self.decoder(states, z))
    vae_mse = mse_loss(actions.features, vae_actions.features)
    vae_kl = nn.kl_loss_vae(mean, log_var)
    vae_loss = (vae_mse + vae_kl)
    self.decoder.reinforce(vae_loss)
    self.encoder.reinforce()
    self.writer.add_scalar('loss/vae/mse', vae_mse.detach())
    self.writer.add_scalar('loss/vae/kl', vae_kl.detach())
    self.writer.train_steps += 1
