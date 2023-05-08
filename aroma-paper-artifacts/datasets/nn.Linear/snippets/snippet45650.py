import os
import time
import torch
from torch.autograd import Variable
from seq2sql.model_seq2seq_base import modelSeq2SeqBase
from LeafNATS.data.seq2sql.process_batch_cqa_v1 import process_batch
from LeafNATS.modules.embedding.nats_embedding import natsEmbedding
from LeafNATS.modules.encoder.encoder_rnn import EncoderRNN
from LeafNATS.modules.encoder2decoder.nats_encoder2decoder import natsEncoder2Decoder
from LeafNATS.modules.attention.nats_attention_encoder import AttentionEncoder
from LeafNATS.modules.attention.nats_attention_decoder import AttentionDecoder


def build_models(self):
    '\n        build all models.\n        in this model source and target share embeddings\n        '
    self.train_models['embedding'] = natsEmbedding(vocab_size=self.batch_data['vocab_size'], emb_dim=self.args.emb_dim, share_emb_weight=True).to(self.args.device)
    self.train_models['encoder'] = EncoderRNN(self.args.emb_dim, self.args.src_hidden_dim, self.args.nLayers, 'lstm', device=self.args.device).to(self.args.device)
    self.train_models['encoder2decoder'] = natsEncoder2Decoder(src_hidden_size=self.args.src_hidden_dim, trg_hidden_size=self.args.trg_hidden_dim, rnn_network='lstm', device=self.args.device).to(self.args.device)
    self.train_models['decoderRNN'] = torch.nn.LSTMCell((self.args.emb_dim + self.args.trg_hidden_dim), self.args.trg_hidden_dim).to(self.args.device)
    self.train_models['attnEncoder'] = AttentionEncoder(self.args.src_hidden_dim, self.args.trg_hidden_dim, attn_method='luong_general', repetition='temporal').to(self.args.device)
    self.train_models['attnDecoder'] = AttentionDecoder(self.args.trg_hidden_dim, attn_method='luong_general').to(self.args.device)
    self.train_models['wrapDecoder'] = torch.nn.Linear(((self.args.src_hidden_dim * 2) + (self.args.trg_hidden_dim * 2)), self.args.trg_hidden_dim, bias=True).to(self.args.device)
    self.train_models['genPrb'] = torch.nn.Linear(((self.args.emb_dim + (self.args.src_hidden_dim * 2)) + self.args.trg_hidden_dim), 1).to(self.args.device)
    self.train_models['decoder2proj'] = torch.nn.Linear(self.args.trg_hidden_dim, self.args.emb_dim, bias=False).to(self.args.device)
