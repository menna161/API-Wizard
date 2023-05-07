import numpy as np
import gym
from scipy.misc import imresize as resize
from gym.spaces.box import Box
from gym.envs.box2d.car_racing import CarRacing
from vae.vae import ConvVAE
from config import games
from model import SimpleWorldModel
import json


def __init__(self, full_episode=False, pure_world=False):
    super(VAERacingWorld, self).__init__()
    self._internal_counter = 0
    self.z_size = games['vae_racing'].input_size
    self.vae = ConvVAE(batch_size=1, z_size=self.z_size, gpu_mode=False, is_training=False, reuse=True)
    self.vae.load_json((('vae/vae_' + str(self.z_size)) + '.json'))
    self.full_episode = full_episode
    if pure_world:
        high = np.array(([np.inf] * 10))
    else:
        high = np.array(([np.inf] * (self.z_size + 10)))
    self.observation_space = Box((- high), high)
    self._has_rendered = False
    self.real_frame = None
    self.world_model = SimpleWorldModel(obs_size=16, action_size=3, hidden_size=10)
    world_model_path = './log/learn_vae_racing.cma.4.64.best.json'
    self.world_model.load_model(world_model_path)
    self.pure_world_mode = pure_world
