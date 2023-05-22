import torch
from torch.autograd import Variable


def __init__(self, src_hidden_size, trg_hidden_size, attn_method, repetition, src_hidden_doubled=True):
    '\n        src_hidden_size, # source side hidden dimension\n        trg_hidden_size, # target side hidden dimension\n        attn_method, # attention method\n        repetition # approaches handle repetition\n        '
    super().__init__()
    self.method = attn_method.lower()
    self.repetition = repetition
    if (self.method == 'luong_concat'):
        if src_hidden_doubled:
            self.attn_en_in = torch.nn.Linear((src_hidden_size * 2), trg_hidden_size)
        else:
            self.attn_en_in = torch.nn.Linear(src_hidden_size, trg_hidden_size)
        self.attn_de_in = torch.nn.Linear(trg_hidden_size, trg_hidden_size, bias=False)
        self.attn_cv_in = torch.nn.Linear(1, trg_hidden_size, bias=False)
        self.attn_warp_in = torch.nn.Linear(trg_hidden_size, 1, bias=False)
    if (self.method == 'luong_general'):
        if src_hidden_doubled:
            self.attn_in = torch.nn.Linear((src_hidden_size * 2), trg_hidden_size, bias=False)
        else:
            self.attn_in = torch.nn.Linear(src_hidden_size, trg_hidden_size, bias=False)
