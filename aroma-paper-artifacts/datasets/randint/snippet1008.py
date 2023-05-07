import numpy as np
from copy import deepcopy
import math
from Utils.MovingAvegCalculator import MovingAvegCalculator


def select_expand_action(self):
    count = 0
    while True:
        if (count < 20):
            action = self.categorical(self.prior_prob)
        else:
            action = np.random.randint(0, self.action_n)
        if (count > 100):
            return action
        if ((self.children_visit_count[action] > 0) and (count < 10)):
            count += 1
            continue
        if (self.children[action] is None):
            return action
        count += 1
