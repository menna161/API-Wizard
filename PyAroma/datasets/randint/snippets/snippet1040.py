import numpy as np
import random
import os
from Policy.PPO.PPOPolicy import PPOAtariCNN, PPOSmallAtariCNN


def get_action(self, state):
    if (self.policy_name == 'Random'):
        return random.randint(0, (self.action_n - 1))
    elif (self.policy_name == 'PPO'):
        return self.categorical(self.policy_func.get_action(state))
    elif (self.policy_name == 'DistillPPO'):
        return self.categorical(self.policy_func[1].get_action(state))
    else:
        raise NotImplementedError()
