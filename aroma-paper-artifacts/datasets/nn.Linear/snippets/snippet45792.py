import torch
from torch.autograd import Variable
from LeafNATS.modules.attention.nats_attention_decoder import AttentionDecoder
from LeafNATS.modules.attention.nats_attention_encoder import AttentionEncoder


def __init__(self, input_size, src_hidden_size, trg_hidden_size, attn_method, repetition, pointer_net, attn_decoder, rnn_network, device=torch.device('cpu')):
    '\n        LSTM/GRU decoder\n        Seq2Seq attention decoder\n        pointer-generator network decoder\n\n        input_size, # input vector size\n        src_hidden_size, # source side hidden size\n        trg_hidden_size, # target side hidden size\n        attn_method, # alignment methods\n        repetition, # approaches handle repetition\n        pointer_net, # turn on pointer network?\n        attn_decoder, # turn on attention decoder?\n        '
    super(PointerGeneratorDecoder, self).__init__()
    self.input_size = input_size
    self.src_hidden_size = src_hidden_size
    self.trg_hidden_size = trg_hidden_size
    self.attn_method = attn_method.lower()
    self.repetition = repetition
    self.pointer_net = pointer_net
    self.attn_decoder = attn_decoder
    self.rnn_network = rnn_network
    self.device = device
    if (rnn_network == 'lstm'):
        self.rnn_ = torch.nn.LSTMCell((input_size + trg_hidden_size), trg_hidden_size).to(device)
    else:
        self.rnn_ = torch.nn.GRUCell((input_size + trg_hidden_size), trg_hidden_size).to(device)
    self.encoder_attn_layer = AttentionEncoder(src_hidden_size=src_hidden_size, trg_hidden_size=trg_hidden_size, attn_method=attn_method, repetition=repetition).to(device)
    if self.attn_decoder:
        self.decoder_attn_layer = AttentionDecoder(hidden_size=trg_hidden_size, attn_method=attn_method).to(device)
        self.attn_out = torch.nn.Linear(((src_hidden_size * 2) + (trg_hidden_size * 2)), trg_hidden_size).to(device)
    else:
        self.attn_out = torch.nn.Linear(((src_hidden_size * 2) + trg_hidden_size), trg_hidden_size).to(device)
    if self.pointer_net:
        if self.attn_decoder:
            self.pt_out = torch.nn.Linear(((input_size + (src_hidden_size * 2)) + (trg_hidden_size * 2)), 1).to(device)
        else:
            self.pt_out = torch.nn.Linear(((input_size + (src_hidden_size * 2)) + trg_hidden_size), 1).to(device)
