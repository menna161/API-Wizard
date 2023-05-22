import torch
import torch.nn as nn
import torch.nn.functional as F
from torchtext.vocab import Vectors
from ...utils.log import logger
from ...base.model import BaseConfig, BaseModel
from .config import DEVICE, DEFAULT_CONFIG


def __init__(self, args):
    super(TextCNN, self).__init__(args)
    self.class_num = args.class_num
    self.chanel_num = 1
    self.filter_num = args.filter_num
    self.filter_sizes = args.filter_sizes
    self.vocabulary_size = args.vocabulary_size
    self.embedding_dimension = args.embedding_dim
    self.embedding = nn.Embedding(self.vocabulary_size, self.embedding_dimension).to(DEVICE)
    if args.static:
        logger.info('logging word vectors from {}'.format(args.vector_path))
        vectors = Vectors(args.vector_path).vectors
        self.embedding = self.embedding.from_pretrained(vectors, freeze=(not args.non_static)).to(DEVICE)
    if args.multichannel:
        self.embedding2 = nn.Embedding(self.vocabulary_size, self.embedding_dimension).from_pretrained(args.vectors).to(DEVICE)
        self.chanel_num += 1
    else:
        self.embedding2 = None
    self.convs = nn.ModuleList([nn.Conv2d(self.chanel_num, self.filter_num, (size, self.embedding_dimension)) for size in self.filter_sizes]).to(DEVICE)
    self.dropout = nn.Dropout(args.dropout).to(DEVICE)
    self.fc = nn.Linear((len(self.filter_sizes) * self.filter_num), self.class_num).to(DEVICE)
