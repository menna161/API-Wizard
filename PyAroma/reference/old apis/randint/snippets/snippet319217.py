import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from environments.environment import Environment


def reset_env(self):
    'Reset the environment. The list are values are draw randomly. The pointers are initialized at position 0\n        (at left position of the list).\n\n        '
    self.scratchpad_ints = np.random.randint(10, size=self.length)
    current_task_name = self.get_program_from_index(self.current_task_index)
    if ((current_task_name == 'BUBBLE') or (current_task_name == 'BUBBLESORT')):
        init_pointers_pos1 = 0
        init_pointers_pos2 = 0
    elif (current_task_name == 'RESET'):
        while True:
            init_pointers_pos1 = int(np.random.randint(0, self.length))
            init_pointers_pos2 = int(np.random.randint(0, self.length))
            if (not ((init_pointers_pos1 == 0) and (init_pointers_pos2 == 0))):
                break
    elif (current_task_name == 'LSHIFT'):
        while True:
            init_pointers_pos1 = int(np.random.randint(0, self.length))
            init_pointers_pos2 = int(np.random.randint(0, self.length))
            if (not ((init_pointers_pos1 == 0) and (init_pointers_pos2 == 0))):
                break
    elif (current_task_name == 'RSHIFT'):
        while True:
            init_pointers_pos1 = int(np.random.randint(0, self.length))
            init_pointers_pos2 = int(np.random.randint(0, self.length))
            if (not ((init_pointers_pos1 == (self.length - 1)) and (init_pointers_pos2 == (self.length - 1)))):
                break
    elif (current_task_name == 'COMPSWAP'):
        init_pointers_pos1 = int(np.random.randint(0, (self.length - 1)))
        init_pointers_pos2 = int(np.random.choice([init_pointers_pos1, (init_pointers_pos1 + 1)]))
    else:
        raise NotImplementedError('Unable to reset env for this program...')
    self.p1_pos = init_pointers_pos1
    self.p2_pos = init_pointers_pos2
    self.has_been_reset = True
