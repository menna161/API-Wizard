import torch
import torch.nn as nn
import numpy as np


def __init__(self, observation_space, hidden_size, single_branch_size=256, cnn_layers_params=None):
    super().__init__()
    if ('sensor' in observation_space.spaces):
        self._n_non_vis_sensor = observation_space.spaces['sensor'].shape[0]
    else:
        self._n_non_vis_sensor = 0
    if ('auxiliary_sensor' in observation_space.spaces):
        self._n_auxiliary_sensor = observation_space.spaces['auxiliary_sensor'].shape[0]
    else:
        self._n_auxiliary_sensor = 0
    if ('scan' in observation_space.spaces):
        self._n_scan = observation_space.spaces['scan'].shape[0]
    else:
        self._n_scan = 0
    if ('subgoal' in observation_space.spaces):
        self._n_subgoal = observation_space.spaces['subgoal'].shape[0]
    else:
        self._n_subgoal = 0
    if ('subgoal_mask' in observation_space.spaces):
        self._n_subgoal_mask = observation_space.spaces['subgoal_mask'].shape[0]
    else:
        self._n_subgoal_mask = 0
    if ('action_mask' in observation_space.spaces):
        self._n_action_mask = observation_space.spaces['action_mask'].shape[0]
    else:
        self._n_action_mask = 0
    self._n_additional_rnn_input = (((((self._n_non_vis_sensor + self._n_auxiliary_sensor) + self._n_subgoal) + self._n_subgoal_mask) + self._n_action_mask) + self._n_scan)
    self._hidden_size = hidden_size
    self._single_branch_size = single_branch_size
    if (self._n_additional_rnn_input != 0):
        self.feature_linear = nn.Sequential(nn.Linear(self._n_additional_rnn_input, self._single_branch_size), nn.ReLU())
    if (cnn_layers_params is None):
        self._cnn_layers_params = [(32, 8, 4, 0), (64, 4, 2, 0), (64, 3, 1, 0)]
    else:
        self._cnn_layers_params = cnn_layers_params
    self.cnn = self._init_perception_model(observation_space)
    self._rnn_input_size = 0
    if (not self.is_blind):
        self._rnn_input_size += single_branch_size
    if (self._n_additional_rnn_input != 0):
        self._rnn_input_size += single_branch_size
    assert (self._rnn_input_size != 0), 'the network has no input'
    self.rnn = nn.GRU(self._rnn_input_size, self._hidden_size)
    self.critic_linear = nn.Linear(self._hidden_size, 1)
    self.layer_init()
    self.train()
