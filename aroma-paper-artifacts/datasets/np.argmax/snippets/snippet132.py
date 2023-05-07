import torch
import numpy as np
import estorch
from cartpole_es import Policy, Agent


def log(self):
    'This function is executed after every optimization. So it can be used \n        to interact with the system during training.'
    idx = np.argmax(self.population_returns)
    reward = self.population_returns[(idx, 0)]
    print(f'Reward: {reward}')
    if (reward == 500):
        self.best = self.population_parameters[idx]
        self.terminate()
