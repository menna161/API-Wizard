import torch
import torch.nn as nn
import torch.nn.functional as F
from net.utils.graph import Graph_J, Graph_P, Graph_B
from net.utils.module import *
from net.utils.operation import PartLocalInform, BodyLocalInform


def __init__(self, n_in_enc, n_hid_enc, n_in_dec, n_hid_dec, graph_args_j, graph_args_p, graph_args_b, fusion_layer, cross_w, **kwargs):
    super().__init__()
    self.encoder_pos = Encoder(n_in_enc, graph_args_j, graph_args_p, graph_args_b, True, fusion_layer, cross_w, **kwargs)
    self.encoder_vel = Encoder(n_in_enc, graph_args_j, graph_args_p, graph_args_b, True, fusion_layer, cross_w, **kwargs)
    self.encoder_acl = Encoder(n_in_enc, graph_args_j, graph_args_p, graph_args_b, True, fusion_layer, cross_w, **kwargs)
    self.decoder = Decoder(n_in_dec, n_hid_dec, graph_args_j, **kwargs)
    self.linear = nn.Linear((n_hid_enc * 3), n_hid_dec)
    self.relu = nn.ReLU()
