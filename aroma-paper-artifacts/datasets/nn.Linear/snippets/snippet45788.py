import torch
from torch.autograd import Variable


def __init__(self, hidden_size, attn_method):
    '\n        hidden_size, # decoder hidden dimension\n        attn_method # alignment method\n        '
    super().__init__()
    self.method = attn_method.lower()
    self.hidden_size = hidden_size
    if (self.method == 'luong_concat'):
        self.attn_en_in = torch.nn.Linear(self.hidden_size, self.hidden_size, bias=True)
        self.attn_de_in = torch.nn.Linear(self.hidden_size, self.hidden_size, bias=False)
        self.attn_warp_in = torch.nn.Linear(self.hidden_size, 1, bias=False)
    if (self.method == 'luong_general'):
        self.attn_in = torch.nn.Linear(self.hidden_size, self.hidden_size, bias=False)
