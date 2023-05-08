import torch
from torch.nn.init import xavier_normal_
import torch.nn as nn
import torch.nn.functional as F
from bert_feature_extractor import BertLayer
from decoder import DistMult, ConvE, ConvTransE, ConvKB
import layers


def __init__(self, num_nodes, num_rels, args, use_cuda=False):
    super(LinkPredictor, self).__init__()
    self.rgcn = GCN(num_nodes, (num_rels * 2), args, use_cuda)
    if args.sim_relations:
        decoder_rels = ((num_rels - 1) * 2)
    else:
        decoder_rels = (num_rels * 2)
    if (args.decoder == 'ConvE'):
        self.decoder = ConvE(num_nodes, decoder_rels, args)
    elif (args.decoder == 'ConvTransE'):
        self.decoder = ConvTransE(num_nodes, decoder_rels, args)
    elif (args.decoder == 'ConvKB'):
        self.decoder = ConvKB(num_nodes, decoder_rels, args)
    else:
        self.decoder = DistMult(num_nodes, decoder_rels, args)
    self.decoder.init()
    self.num_rels = num_rels
    self.num_nodes = num_nodes
    self.use_cuda = use_cuda
    self.reg_param = args.regularization
    self.input_layer = args.input_layer
    self.bert_concat = args.bert_concat
    self.bert_sum = args.bert_sum
    self.bert_mlp = args.bert_mlp
    self.tying = args.tying
    self.layer_norm = args.layer_norm
    self.bert_dim = 1024
    if self.bert_concat:
        self.bert_concat_layer = EmbeddingLayer(num_nodes, self.bert_dim, args.dataset, init_bert=True)
    if self.bert_sum:
        self.bert_concat_layer = EmbeddingLayer(num_nodes, self.bert_dim, args.dataset, init_bert=True)
        self.beta = 0.5
    if self.bert_mlp:
        self.bert_concat_layer = EmbeddingLayer(num_nodes, self.bert_dim, args.dataset, init_bert=True)
        self.bmlp = nn.Linear((self.bert_dim + 200), 600)
    if self.layer_norm:
        self.bert_norm = nn.LayerNorm(self.bert_dim)
        self.gcn_norm = nn.LayerNorm(args.embedding_dim)
