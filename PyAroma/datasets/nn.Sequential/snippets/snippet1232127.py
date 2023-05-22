import torch
import torch.nn as nn
import numpy as np


def _init_perception_model(self, observation_space):
    if ('rgb' in observation_space.spaces):
        self._n_input_rgb = observation_space.spaces['rgb'].shape[2]
    else:
        self._n_input_rgb = 0
    if ('depth' in observation_space.spaces):
        self._n_input_depth = observation_space.spaces['depth'].shape[2]
    else:
        self._n_input_depth = 0
    if ('global_map' in observation_space.spaces):
        self._n_input_global_map = observation_space.spaces['global_map'].shape[0]
    else:
        self._n_input_global_map = 0
    if ('local_map' in observation_space.spaces):
        self._n_input_local_map = observation_space.spaces['local_map'].shape[0]
    else:
        self._n_input_local_map = 0
    if (self._n_input_rgb > 0):
        cnn_dims = np.array(observation_space.spaces['rgb'].shape[:2], dtype=np.float32)
    elif (self._n_input_depth > 0):
        cnn_dims = np.array(observation_space.spaces['depth'].shape[:2], dtype=np.float32)
    elif (self._n_input_global_map > 0):
        cnn_dims = np.array(observation_space.spaces['global_map'].shape[1:3], dtype=np.float32)
    elif (self._n_input_local_map > 0):
        cnn_dims = np.array(observation_space.spaces['local_map'].shape[1:3], dtype=np.float32)
    if self.is_blind:
        return nn.Sequential()
    else:
        for (_, kernel_size, stride, padding) in self._cnn_layers_params:
            cnn_dims = self._conv_output_dim(dimension=cnn_dims, padding=np.array([padding, padding], dtype=np.float32), dilation=np.array([1, 1], dtype=np.float32), kernel_size=np.array([kernel_size, kernel_size], dtype=np.float32), stride=np.array([stride, stride], dtype=np.float32))
        cnn_layers = []
        prev_out_channels = None
        for (i, (out_channels, kernel_size, stride, padding)) in enumerate(self._cnn_layers_params):
            if (i == 0):
                in_channels = (((self._n_input_rgb + self._n_input_depth) + self._n_input_global_map) + self._n_input_local_map)
            else:
                in_channels = prev_out_channels
            cnn_layers.append(nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, stride=stride, padding=padding))
            if (i != (len(self._cnn_layers_params) - 1)):
                cnn_layers.append(nn.ReLU())
            prev_out_channels = out_channels
        cnn_layers += [Flatten(), nn.Linear(((self._cnn_layers_params[(- 1)][0] * cnn_dims[0]) * cnn_dims[1]), self._single_branch_size), nn.ReLU()]
        return nn.Sequential(*cnn_layers)
