import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torch.distributions.categorical import Categorical
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import babyai.rl
from babyai.rl.utils.supervised_losses import required_heads


def __init__(self, obs_space, action_space, image_dim=128, memory_dim=128, instr_dim=128, use_desc=True, lang_model='gru', use_memory=False, arch='cnn', aux_info=None, random_shuffled=False, instr_sents=2, enable_instr=False, instr_only=False):
    super().__init__()
    self.use_desc = use_desc
    self.use_memory = use_memory
    self.random_shuffled = random_shuffled
    self.enable_instr = enable_instr
    self.instr_only = instr_only
    self.arch = arch
    self.lang_model = lang_model
    self.aux_info = aux_info
    self.image_dim = image_dim
    self.memory_dim = memory_dim
    self.instr_dim = instr_dim
    self.instr_sents = instr_sents
    self.obs_space = obs_space
    if (arch == 'cnn'):
        self.image_conv = nn.Sequential(nn.Conv2d(in_channels=3, out_channels=128, kernel_size=(2, 2)), nn.BatchNorm2d(128), nn.ReLU(), nn.MaxPool2d(kernel_size=(2, 2), stride=2), nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(3, 3), padding=1), nn.BatchNorm2d(128), nn.ReLU(), nn.MaxPool2d(kernel_size=(2, 2), stride=2))
    elif arch.startswith('expert_filmcnn'):
        if (not self.use_desc):
            raise ValueError('FiLM architecture can be used when instructions are enabled')
        self.image_conv = nn.Sequential(nn.Conv2d(in_channels=3, out_channels=128, kernel_size=(2, 2), padding=1), nn.BatchNorm2d(128), nn.ReLU(), nn.MaxPool2d(kernel_size=(2, 2), stride=2), nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(3, 3), padding=1), nn.BatchNorm2d(128), nn.ReLU(), nn.MaxPool2d(kernel_size=(2, 2), stride=2))
        self.film_pool = nn.MaxPool2d(kernel_size=(2, 2), stride=2)
    elif (arch == 'fusion'):
        if (not self.use_desc):
            raise ValueError('fusion architecture can be used when instructions are enabled')
        self.image_conv = nn.Sequential(nn.Conv2d(in_channels=3, out_channels=128, kernel_size=(3, 3), padding=1), nn.BatchNorm2d(128), nn.ReLU(), nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(3, 3), padding=1), nn.BatchNorm2d(128), nn.ReLU())
        self.w_conv = nn.Sequential(nn.Conv2d(in_channels=3, out_channels=128, kernel_size=(3, 3), padding=1), nn.BatchNorm2d(128), nn.ReLU(), nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(3, 3), padding=1), nn.BatchNorm2d(128), nn.ReLU(), nn.Conv2d(in_channels=128, out_channels=(self.instr_sents + 1), kernel_size=(3, 3), padding=1))
        self.combined_conv = nn.Sequential(nn.Conv2d(in_channels=256, out_channels=128, kernel_size=(2, 2)), nn.ReLU(), nn.MaxPool2d(kernel_size=(2, 2), stride=2), nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(2, 2)), nn.ReLU(), nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(2, 2)), nn.ReLU())
        '\n            self.image_conv = nn.Sequential(\n                nn.Conv2d(in_channels=3, out_channels=128, kernel_size=(3, 3), padding=1),\n                nn.BatchNorm2d(128),\n                nn.ReLU(),\n                # nn.MaxPool2d(kernel_size=(2, 2), stride=2),\n                nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(3, 3), padding=1),\n                nn.BatchNorm2d(128),\n                nn.ReLU(),\n                # nn.MaxPool2d(kernel_size=(2, 2), stride=2)\n            )\n            self.w_conv = nn.Conv2d(in_channels=128, out_channels=self.instr_sents, kernel_size=(3, 3), padding=1).cuda()\n            self.combined_conv = nn.Sequential(\n                nn.Conv2d(in_channels=256, out_channels=128, kernel_size=(2, 2)),\n                nn.ReLU(),\n                nn.MaxPool2d(kernel_size=(2, 2), stride=2),\n                nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(2, 2)),\n                nn.ReLU(),\n                nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(2, 2)),\n                nn.ReLU()\n            ) \n            '
    else:
        raise ValueError('Incorrect architecture name: {}'.format(arch))
    if self.use_desc:
        if (self.lang_model in ['gru', 'bigru', 'attgru']):
            self.word_embedding = nn.Embedding(obs_space['instr'], self.instr_dim)
            if (self.lang_model in ['gru', 'bigru', 'attgru']):
                gru_dim = self.instr_dim
                if (self.lang_model in ['bigru', 'attgru']):
                    gru_dim //= 2
                self.instr_rnn = nn.GRU(self.instr_dim, gru_dim, batch_first=True, bidirectional=(self.lang_model in ['bigru', 'attgru']))
                self.final_instr_dim = self.instr_dim
            else:
                kernel_dim = 64
                kernel_sizes = [3, 4]
                self.instr_convs = nn.ModuleList([nn.Conv2d(1, kernel_dim, (K, self.instr_dim)) for K in kernel_sizes])
                self.final_instr_dim = (kernel_dim * len(kernel_sizes))
        if (self.lang_model == 'attgru'):
            self.memory2key = nn.Linear(self.memory_size, self.final_instr_dim)
    if self.use_memory:
        self.memory_rnn = nn.LSTMCell(self.image_dim, self.memory_dim)
    self.embedding_size = self.semi_memory_size
    if (self.use_desc and (not ('filmcnn' in arch)) and (not ('fusion' in arch))):
        self.embedding_size += self.final_instr_dim
    if (arch.startswith('expert_filmcnn') or ((self.arch == 'fusion') and self.enable_instr)):
        num_module = 2
        self.controllers = []
        for ni in range(num_module):
            if (ni < (num_module - 1)):
                mod = ExpertControllerFiLM(in_features=self.final_instr_dim, out_features=128, in_channels=128, imm_channels=128)
            else:
                mod = ExpertControllerFiLM(in_features=self.final_instr_dim, out_features=self.image_dim, in_channels=128, imm_channels=128)
            self.controllers.append(mod)
            self.add_module(('FiLM_Controler_' + str(ni)), mod)
    self.actor = nn.Sequential(nn.Linear(self.embedding_size, 64), nn.Tanh(), nn.Linear(64, action_space.n))
    self.critic = nn.Sequential(nn.Linear(self.embedding_size, 64), nn.Tanh(), nn.Linear(64, 1))
    self.apply(initialize_parameters)
    if self.aux_info:
        self.extra_heads = None
        self.add_heads()
