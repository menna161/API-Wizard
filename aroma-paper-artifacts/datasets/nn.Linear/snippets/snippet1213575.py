import torch
from torch import nn, optim
import torch.nn.functional as F
from torchtext import data
from torch.utils.data import DataLoader
from torchtext.data import Iterator
from gensim.models import KeyedVectors


def __init__(self, output_dim, kernel_num, kernel_sizes=[3, 4, 5], dropout=0.5, static=False):
    super(CNN, self).__init__()
    model = KeyedVectors.load_word2vec_format('ch07/GoogleNews-vectors-negative300.bin', binary=True)
    weights = torch.FloatTensor(model.vectors)
    self.embed = nn.Embedding.from_pretrained(weights)
    self.convs1 = nn.ModuleList([nn.Conv2d(1, kernel_num, (k, self.embed.weight.shape[1])) for k in kernel_sizes])
    self.dropout = nn.Dropout(dropout)
    self.fc1 = nn.Linear((len(kernel_sizes) * kernel_num), output_dim)
    self.static = static
