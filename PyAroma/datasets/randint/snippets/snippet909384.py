import numpy as np
from .experience_buffer import ExperienceBuffer
from .actor import Actor
from .critic import Critic
from .normalize import Normalizer
from .Curiosity import ForwardDynamics


def finalize_goal_replay(self, goal_thresholds):
    num_trans = len(self.temp_goal_replay_storage)
    num_replay_goals = self.num_replay_goals
    if (num_trans < self.num_replay_goals):
        num_replay_goals = num_trans
    indices = np.zeros(num_replay_goals)
    indices[:(num_replay_goals - 1)] = np.random.randint(num_trans, size=(num_replay_goals - 1))
    indices[(num_replay_goals - 1)] = (num_trans - 1)
    indices = np.sort(indices)
    for i in range(len(indices)):
        trans_copy = np.copy(self.temp_goal_replay_storage)
        new_goal = trans_copy[int(indices[i])][6]
        for index in range(num_trans):
            trans_copy[index][4] = new_goal
            trans_copy[index][2] = self.get_reward(new_goal, trans_copy[index][6], goal_thresholds, self.FLAGS.rtype)
            if (trans_copy[index][2] == 0):
                trans_copy[index][5] = True
            else:
                trans_copy[index][5] = False
            self.replay_buffer.add(trans_copy[index])
    self.temp_goal_replay_storage = []
