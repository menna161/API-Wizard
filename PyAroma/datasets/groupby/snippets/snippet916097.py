from typing import Dict, List, Tuple, Union
import numpy as np
import pandas as pd
from gym import Env
from gym import spaces


def __init__(self, data: pd.DataFrame, item: pd.DataFrame, user: pd.DataFrame, seed: int=1):
    '\n        Parameterized constructor\n        '
    self.data = data
    self.item = item
    self.user = user
    self.movie_genre = self._get_movie_genre(item=self.item)
    self.user_info = self._get_user_data(user=self.user)
    self.occupations = self.user.occupation.unique().tolist()
    self.num_of_occupations = len(self.occupations)
    self.user_mean = self.data.groupby('user_id').mean().to_dict()['rating']
    self.movie_mean = self.data.groupby('item_id').mean().to_dict()['rating']
    self.reward = 0.0
    self.done = False
    self.observation = None
    self.action = 0
    self.local_step_number = 0
    self._seed = seed
    self._random_state = np.random.RandomState(seed=self._seed)
    self.max_step = (self.data.shape[0] - 2)
    self.total_correct_predictions = 0
    self.data = self.data.values
    self.action_space = spaces.Discrete(len(RecoEnv.actions))
    self.observation_space = spaces.Box(low=(- 1.0), high=5.0, shape=self._get_observation(step_number=0).shape, dtype=np.float32)
