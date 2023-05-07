from typing import Dict, Iterator, List
import torch
import torch.nn as nn
from torch.autograd import Variable
from allennlp.modules.text_field_embedders import TextFieldEmbedder
from allennlp.modules.matrix_attention.cosine_matrix_attention import CosineMatrixAttention


def __init__(self, word_embeddings_out_dim: int):
    super(Duet, self).__init__()
    NUM_HIDDEN_NODES = word_embeddings_out_dim
    POOLING_KERNEL_WIDTH_QUERY = 18
    POOLING_KERNEL_WIDTH_DOC = 100
    DROPOUT_RATE = 0
    NUM_POOLING_WINDOWS_DOC = 99
    MAX_DOC_TERMS = 2000
    MAX_QUERY_TERMS = 30
    self.cosine_module = CosineMatrixAttention()
    self.duet_local = nn.Sequential(nn.Conv1d(MAX_DOC_TERMS, NUM_HIDDEN_NODES, kernel_size=1), nn.ReLU(), Flatten(), nn.Dropout(p=DROPOUT_RATE), nn.Linear((NUM_HIDDEN_NODES * MAX_QUERY_TERMS), NUM_HIDDEN_NODES), nn.ReLU(), nn.Dropout(p=DROPOUT_RATE), nn.Linear(NUM_HIDDEN_NODES, NUM_HIDDEN_NODES), nn.ReLU(), nn.Dropout(p=DROPOUT_RATE))
    self.duet_dist_q = nn.Sequential(nn.Conv1d(NUM_HIDDEN_NODES, NUM_HIDDEN_NODES, kernel_size=3), nn.ReLU(), nn.MaxPool1d(POOLING_KERNEL_WIDTH_QUERY), Flatten(), nn.Linear(NUM_HIDDEN_NODES, NUM_HIDDEN_NODES), nn.ReLU())
    self.duet_dist_d = nn.Sequential(nn.Conv1d(NUM_HIDDEN_NODES, NUM_HIDDEN_NODES, kernel_size=3), nn.ReLU(), nn.MaxPool1d(POOLING_KERNEL_WIDTH_DOC, stride=1), nn.Conv1d(NUM_HIDDEN_NODES, NUM_HIDDEN_NODES, kernel_size=1), nn.ReLU())
    self.duet_dist = nn.Sequential(Flatten(), nn.Dropout(p=DROPOUT_RATE), nn.Linear((NUM_HIDDEN_NODES * NUM_POOLING_WINDOWS_DOC), NUM_HIDDEN_NODES), nn.ReLU(), nn.Dropout(p=DROPOUT_RATE), nn.Linear(NUM_HIDDEN_NODES, NUM_HIDDEN_NODES), nn.ReLU(), nn.Dropout(p=DROPOUT_RATE))
    self.duet_comb = nn.Sequential(nn.Linear(NUM_HIDDEN_NODES, NUM_HIDDEN_NODES), nn.ReLU(), nn.Dropout(p=DROPOUT_RATE), nn.Linear(NUM_HIDDEN_NODES, NUM_HIDDEN_NODES), nn.ReLU(), nn.Dropout(p=DROPOUT_RATE), nn.Linear(NUM_HIDDEN_NODES, 1), nn.ReLU())

    def init_normal(m):
        if (type(m) == nn.Linear):
            nn.init.uniform_(m.weight, 0, 0.01)
    self.duet_comb.apply(init_normal)
