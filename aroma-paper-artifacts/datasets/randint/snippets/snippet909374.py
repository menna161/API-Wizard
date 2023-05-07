import numpy as np
from .normalize import Normalizer


def get_batch(self):
    (states, actions, rewards, new_states, goals, is_terminals) = ([], [], [], [], [], [])
    dist = np.random.randint(0, high=self.size, size=self.batch_size)
    for i in dist:
        if (self.if_normalize and (self.state_norm is not None) and (self.goal_norm is not None)):
            states.append(self.state_norm.normalize(self.experiences[i][0]))
            new_states.append(self.state_norm.normalize(self.experiences[i][3]))
            goals.append(self.goal_norm.normalize(self.experiences[i][4]))
        else:
            states.append(self.experiences[i][0])
            new_states.append(self.experiences[i][3])
            goals.append(self.experiences[i][4])
        actions.append(self.experiences[i][1])
        rewards.append(self.experiences[i][2])
        is_terminals.append(self.experiences[i][5])
    return (states, actions, rewards, new_states, goals, is_terminals)
