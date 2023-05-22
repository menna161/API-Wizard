import torch
import torch.nn as nn
from torchcrf import CRF
from torchtext.vocab import Vectors
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from ...utils.log import logger
from .config import DEVICE, DEFAULT_CONFIG
from ...base.model import BaseConfig, BaseModel


def __init__(self, args):
    super(BiLstmCrf, self).__init__(args)
    self.args = args
    self.hidden_dim = 300
    self.tag_num = args.tag_num
    self.batch_size = args.batch_size
    self.bidirectional = True
    self.num_layers = args.num_layers
    self.pad_index = args.pad_index
    self.dropout = args.dropout
    self.save_path = args.save_path
    vocabulary_size = args.vocabulary_size
    embedding_dimension = args.embedding_dim
    pos_size = args.pos_size
    pos_dim = args.pos_dim
    self.word_embedding = nn.Embedding(vocabulary_size, embedding_dimension).to(DEVICE)
    if args.static:
        logger.info('logging word vectors from {}'.format(args.vector_path))
        vectors = Vectors(args.vector_path).vectors
        self.word_embedding = nn.Embedding.from_pretrained(vectors, freeze=(not args.non_static)).to(DEVICE)
    self.pos_embedding = nn.Embedding(pos_size, pos_dim).to(DEVICE)
    self.lstm = nn.LSTM(((embedding_dimension + pos_dim) + 1), (self.hidden_dim // 2), bidirectional=self.bidirectional, num_layers=self.num_layers, dropout=self.dropout).to(DEVICE)
    self.hidden2label = nn.Linear(self.hidden_dim, self.tag_num).to(DEVICE)
    self.crflayer = CRF(self.tag_num).to(DEVICE)
