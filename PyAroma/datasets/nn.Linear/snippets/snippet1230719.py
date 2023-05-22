import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torch.distributions.categorical import Categorical
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import babyai.rl
from babyai.rl.utils.supervised_losses import required_heads


def add_heads(self):
    '\n        When using auxiliary tasks, the environment yields at each step some binary, continous, or multiclass\n        information. The agent needs to predict those information. This function add extra heads to the model\n        that output the predictions. There is a head per extra information (the head type depends on the extra\n        information type).\n        '
    self.extra_heads = nn.ModuleDict()
    for info in self.aux_info:
        if (required_heads[info] == 'binary'):
            self.extra_heads[info] = nn.Linear(self.embedding_size, 1)
        elif required_heads[info].startswith('multiclass'):
            n_classes = int(required_heads[info].split('multiclass')[(- 1)])
            self.extra_heads[info] = nn.Linear(self.embedding_size, n_classes)
        elif required_heads[info].startswith('continuous'):
            if required_heads[info].endswith('01'):
                self.extra_heads[info] = nn.Sequential(nn.Linear(self.embedding_size, 1), nn.Sigmoid())
            else:
                raise ValueError('Only continous01 is implemented')
        else:
            raise ValueError('Type not supported')
        self.extra_heads[info].apply(initialize_parameters)
