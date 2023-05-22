import torch
import gym
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from dataclasses import dataclass
from typing import Any
from random import random


def train_actor(actor_model, critic_model, state_transitions, num_actor_training_samples, num_actions):
    random_actions = []
    for i in range(num_actor_training_samples):
        random_actions.append(((np.random.rand(num_actions) * 2) - 1))
    random_states = [s.state for s in state_transitions]
    for i in range(len(random_states)):
        with torch.no_grad():
            act = actor_model(torch.Tensor(random_states[i]).to(actor_model.device)).cpu().detach().numpy()
            random_actions.append(act)
    best_state_action = []
    for i_states in range(len(random_states)):
        QAs = []
        for i_actions in range(len(random_actions)):
            with torch.no_grad():
                qval = critic_model(torch.Tensor(torch.cat((torch.Tensor(random_states[i_states]), torch.Tensor(random_actions[i_actions])), 0)).to(critic_model.device)).cpu()
                QAs.append(qval)
        best_state_action.append(sars(random_states[i_states], random_actions[np.argmax(QAs)], 0.0, None, False, np.max(QAs)))
    t_random_states = torch.stack([torch.Tensor(s.state) for s in best_state_action]).to(actor_model.device)
    target_actions = torch.stack([torch.Tensor(s.action) for s in best_state_action]).to(actor_model.device)
    actor_model.zero_grad()
    predicted_actions = actor_model(t_random_states)
    loss = F.smooth_l1_loss(predicted_actions, target_actions).mean()
    loss.backward()
    actor_model.opt.step()
    return loss
