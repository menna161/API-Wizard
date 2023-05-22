import torch
import torch.nn as nn
import torch.nn.functional as F
from torchtext.vocab import Vectors
from ...utils.log import logger
from ...base.model import BaseConfig, BaseModel
from .config import DEVICE, DEFAULT_CONFIG


def __init__(self, args):
    super(LSTMClassifier, self).__init__(args)
    self.hidden_dim = 300
    self.class_num = args.class_num
    self.batch_size = args.batch_size
    self.vocabulary_size = args.vocabulary_size
    self.embedding_dimension = args.embedding_dim
    self.embedding = nn.Embedding(self.vocabulary_size, self.embedding_dimension).to(DEVICE)
    if args.static:
        self.embedding = self.embedding.from_pretrained(args.vectors, freeze=(not args.non_static)).to(DEVICE)
    if args.multichannel:
        self.embedding2 = nn.Embedding(self.vocabulary_size, self.embedding_dimension).from_pretrained(args.vectors).to(DEVICE)
    else:
        self.embedding2 = None
    self.lstm = nn.LSTM(self.embedding_dimension, self.hidden_dim).to(DEVICE)
    self.hidden2label = nn.Linear(self.hidden_dim, self.class_num).to(DEVICE)
    self.hidden = self.init_hidden()
