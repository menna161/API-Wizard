import os
import torch
from torch.distributions.normal import Normal
from torch.nn.functional import mse_loss
from copy import deepcopy
from rlil.environments import State, action_decorator, Action
from rlil.initializer import get_writer, get_device, get_replay_buffer
from rlil import nn
from .base import Agent, LazyAgent


def train(self):
    (states, actions, rewards, next_states, _, _) = self.replay_buffer.sample(self.minibatch_size)
    (mean, log_var) = self.encoder(states.to(self.device), actions.to(self.device))
    z = (mean + ((0.5 * log_var).exp() * torch.randn_like(log_var)))
    vae_actions = Action(self.decoder(states, z))
    vae_mse = mse_loss(actions.features, vae_actions.features)
    vae_kl = nn.kl_loss_vae(mean, log_var)
    vae_loss = (vae_mse + (0.5 * vae_kl))
    self.decoder.reinforce(vae_loss)
    self.encoder.reinforce()
    self.writer.add_scalar('loss/vae/mse', vae_mse.detach())
    self.writer.add_scalar('loss/vae/kl', vae_kl.detach())
    with torch.no_grad():
        next_states_10 = State(torch.repeat_interleave(next_states.features, 10, 0).to(self.device))
        next_vae_actions = Action(self.decoder(next_states_10))
        next_actions = Action(self.policy.target(next_states_10, next_vae_actions))
        q_1_targets = self.q_1.target(next_states_10, next_actions)
        q_2_targets = self.q_2.target(next_states_10, next_actions)
        q_targets = ((self.lambda_q * torch.min(q_1_targets, q_2_targets)) + ((1.0 - self.lambda_q) * torch.max(q_1_targets, q_2_targets)))
        q_targets = q_targets.reshape(self.minibatch_size, (- 1)).max(1)[0].reshape((- 1), 1)
        q_targets = (rewards.reshape((- 1), 1) + ((self.discount_factor * q_targets) * next_states.mask.float().reshape((- 1), 1)))
    self.q_1.reinforce(mse_loss(self.q_1(states, actions).reshape((- 1), 1), q_targets))
    self.q_2.reinforce(mse_loss(self.q_2(states, actions).reshape((- 1), 1), q_targets))
    vae_actions = Action(self.decoder(states))
    sampled_actions = Action(self.policy(states, vae_actions))
    loss = (- self.q_1(states, sampled_actions).mean())
    self.policy.reinforce(loss)
    self.writer.train_steps += 1
