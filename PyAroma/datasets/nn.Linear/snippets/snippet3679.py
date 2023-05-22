import torch
from torch import nn
import numpy as np
from modeling_rel.word_vecs import obj_edge_vectors
from core.config import cfg
import torch.nn.functional as F
from torch.autograd import Variable


def __init__(self, dim_in, embed_dim, dim_out):
    super(Merge_OBJ_Feats, self).__init__()
    self.dim_in = dim_in
    self.embed_dim = embed_dim
    self.dim_out = dim_out
    classes = cfg.LANGUAGE.OBJS_CLASSES
    assert (cfg.MODEL.NUM_CLASSES == len(classes))
    classes = [s.lower() for s in classes]
    self.pos_embed = nn.Sequential(*[nn.BatchNorm1d(4, momentum=(0.01 / 10.0)), nn.Linear(4, 128), nn.ReLU(inplace=True), nn.Dropout(0.1)])
    self.obj_embed = nn.Embedding(cfg.MODEL.NUM_CLASSES, self.embed_dim)
    obj_wvs = obj_edge_vectors(classes, wv_dim=self.embed_dim)
    self.obj_embed.weight.data = obj_wvs.clone()
    self.reduce_dim = nn.Linear(((self.dim_in + self.embed_dim) + 128), self.dim_out)
