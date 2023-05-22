import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


def __init__(self, word_size, word_dim, hidden_dim, disc_size):
    super(DenoiseSum, self).__init__()
    self.word_size = word_size
    self.word_dim = word_dim
    self.hidden_dim = hidden_dim
    self.fuse = fuse
    self.disc_type = disc_type
    self.word_embs = nn.Embedding(num_embeddings=word_size, embedding_dim=word_dim, padding_idx=0)
    self.fw_encoder = nn.LSTMCell(word_dim, (hidden_dim // 2))
    self.bw_encoder = nn.LSTMCell(word_dim, (hidden_dim // 2))
    self.dns_att_key = nn.Linear(hidden_dim, hidden_dim)
    self.dns_att_query = nn.Linear(hidden_dim, hidden_dim)
    self.dns_pnt_key = nn.Linear(hidden_dim, hidden_dim)
    self.dns_pnt_query = nn.Linear(hidden_dim, hidden_dim)
    self.fse_att_key = nn.Linear(hidden_dim, hidden_dim)
    self.fse_pnt_key = nn.Linear(hidden_dim, hidden_dim)
    self.fse_att_transform = nn.Linear(hidden_dim, (hidden_dim // 2))
    self.fse_pnt_transform = nn.Linear(hidden_dim, (hidden_dim // 2))
    self.dsc_intermediate = nn.Linear(hidden_dim, hidden_dim)
    self.dsc_classifier = nn.Linear(hidden_dim, disc_size)
    self.att_decoder = nn.LSTMCell(word_dim, (hidden_dim // 2))
    self.att_key = nn.Linear(hidden_dim, (hidden_dim // 2))
    self.att_query = nn.Linear((hidden_dim // 2), (hidden_dim // 2))
    self.att_weight = nn.Linear((hidden_dim // 2), 1)
    self.att_ctx_classifier = nn.Linear(hidden_dim, word_size)
    self.att_hid_classifier = nn.Linear((hidden_dim // 2), word_size)
    self.att_coverage = nn.Linear(1, (hidden_dim // 2))
    self.pnt_decoder = nn.LSTMCell(word_dim, (hidden_dim // 2))
    self.pnt_key = nn.Linear(hidden_dim, (hidden_dim // 2))
    self.pnt_query = nn.Linear((hidden_dim // 2), (hidden_dim // 2))
    self.pnt_weight = nn.Linear((hidden_dim // 2), 1)
    self.pnt_ctx_classifier = nn.Linear(hidden_dim, word_size)
    self.pnt_hid_classifier = nn.Linear((hidden_dim // 2), word_size)
    self.pnt_gate = nn.Linear(((hidden_dim * 3) // 2), 1)
    self.pnt_coverage = nn.Linear(1, (hidden_dim // 2))
    self.final_gate = nn.Linear(((hidden_dim * 3) // 2), 1)
    self.dropout = nn.Dropout(0.1)
