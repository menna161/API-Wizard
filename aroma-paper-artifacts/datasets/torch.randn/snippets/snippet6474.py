import os
import torch
import numpy as np
from torch.distributions.normal import Normal
from torch.nn.functional import mse_loss
from copy import deepcopy
from rlil.environments import State, action_decorator, Action
from rlil.initializer import get_writer, get_device, get_replay_buffer
from rlil import nn
from .base import Agent, LazyAgent


def train(self):
    self._train_count += 1
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
        next_vae_actions_10 = Action(self.decoder(next_states_10))
        next_actions_10 = Action(self.policy.target(next_states_10, next_vae_actions_10))
        qs_targets = self.qs.target(next_states_10, next_actions_10)
        q_targets = ((self.lambda_q * qs_targets.min(1)[0]) + ((1.0 - self.lambda_q) * qs_targets.max(1)[0]))
        q_targets = q_targets.reshape(self.minibatch_size, (- 1)).max(1)[0].reshape((- 1), 1)
        q_targets = (rewards.reshape((- 1), 1) + ((self.discount_factor * q_targets) * next_states.mask.float().reshape((- 1), 1)))
    current_qs = self.qs(states, actions)
    repeated_q_targets = torch.repeat_interleave(q_targets, current_qs.shape[1], 1)
    q_loss = mse_loss(current_qs, repeated_q_targets)
    self.qs.reinforce(q_loss)
    (vae_actions, raw_vae_actions) = self.decoder.decode_multiple(states, self.num_samples_match)
    (actor_actions, raw_actor_actions) = self.policy.sample_multiple(states, self.num_samples_match)
    if (self.kernel_type == 'gaussian'):
        mmd = nn.mmd_gaussian(raw_vae_actions, raw_actor_actions, sigma=self.mmd_sigma)
    else:
        mmd = nn.mmd_laplacian(raw_vae_actions, raw_actor_actions, sigma=self.mmd_sigma)
    repeated_states = torch.repeat_interleave(states.features.unsqueeze(1), self.num_samples_match, 1).view((- 1), states.shape[1])
    repeated_actions = actor_actions.contiguous().view((- 1), actor_actions.shape[2])
    critic_qs = self.qs(State(repeated_states), Action(repeated_actions))
    critic_qs = critic_qs.view((- 1), self.num_samples_match, critic_qs.shape[1])
    critic_qs = critic_qs.mean(1)
    std_q = torch.std(critic_qs, dim=(- 1), keepdim=False, unbiased=False)
    critic_qs = critic_qs.min(1)[0]
    if (self._train_count >= 20):
        actor_loss = (((- critic_qs) + ((self._lambda * np.sqrt(((1 - self.delta_conf) / self.delta_conf))) * std_q)) + (self.log_lagrange2.exp().detach() * mmd)).mean()
    else:
        actor_loss = (self.log_lagrange2.exp() * mmd).mean()
    std_loss = ((self._lambda * np.sqrt(((1 - self.delta_conf) / self.delta_conf))) * std_q.detach().mean())
    self.policy.reinforce(actor_loss)
    thresh = 0.05
    lagrange_loss = (self.log_lagrange2.exp() * (mmd - thresh).detach()).mean()
    self.lagrange2_opt.zero_grad()
    (- lagrange_loss).backward()
    self.lagrange2_opt.step()
    self.log_lagrange2.data.clamp_(min=(- 5.0), max=10.0)
    self.writer.add_scalar('loss/mmd', mmd.detach().mean())
    self.writer.add_scalar('loss/actor', actor_loss.detach())
    self.writer.add_scalar('loss/qs', q_loss.detach())
    self.writer.add_scalar('loss/std', std_loss.detach())
    self.writer.add_scalar('loss/lagrange2', lagrange_loss.detach())
    self.writer.add_scalar('critic_qs', critic_qs.detach().mean())
    self.writer.add_scalar('std_q', std_q.detach().mean())
    self.writer.add_scalar('lagrange2', self.log_lagrange2.exp().detach())
    self.writer.train_steps += 1
