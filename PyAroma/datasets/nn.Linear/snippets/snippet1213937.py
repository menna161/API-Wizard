from helper import *


def __init__(self, params, chequer_perm):
    super(InteractE, self).__init__()
    self.p = params
    self.ent_embed = torch.nn.Embedding(self.p.num_ent, self.p.embed_dim, padding_idx=None)
    xavier_normal_(self.ent_embed.weight)
    self.rel_embed = torch.nn.Embedding((self.p.num_rel * 2), self.p.embed_dim, padding_idx=None)
    xavier_normal_(self.rel_embed.weight)
    self.bceloss = torch.nn.BCELoss()
    self.inp_drop = torch.nn.Dropout(self.p.inp_drop)
    self.hidden_drop = torch.nn.Dropout(self.p.hid_drop)
    self.feature_map_drop = torch.nn.Dropout2d(self.p.feat_drop)
    self.bn0 = torch.nn.BatchNorm2d(self.p.perm)
    flat_sz_h = self.p.k_h
    flat_sz_w = (2 * self.p.k_w)
    self.padding = 0
    self.bn1 = torch.nn.BatchNorm2d((self.p.num_filt * self.p.perm))
    self.flat_sz = (((flat_sz_h * flat_sz_w) * self.p.num_filt) * self.p.perm)
    self.bn2 = torch.nn.BatchNorm1d(self.p.embed_dim)
    self.fc = torch.nn.Linear(self.flat_sz, self.p.embed_dim)
    self.chequer_perm = chequer_perm
    self.register_parameter('bias', Parameter(torch.zeros(self.p.num_ent)))
    self.register_parameter('conv_filt', Parameter(torch.zeros(self.p.num_filt, 1, self.p.ker_sz, self.p.ker_sz)))
    xavier_normal_(self.conv_filt)
