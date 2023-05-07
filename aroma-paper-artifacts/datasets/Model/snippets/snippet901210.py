import math
import torch.nn as nn
from onqg.models.Models import UnifiedModel
from onqg.models.Encoders import RNNEncoder, GraphEncoder, EncoderTransformer, SparseGraphEncoder, TransfEncoder
from onqg.models.Decoders import RNNDecoder, DecoderTransformer


def build_model(opt, device, separate=(- 1), checkpoint=None):
    seq_encoder = build_encoder(opt)
    encoder_transformer = EncoderTransformer(opt.d_seq_enc_model, d_k=opt.d_k, device=device)
    graph_encoder = build_encoder(opt, graph=True)
    if (opt.d_seq_enc_model != opt.d_graph_enc_model):
        graph_encoder.activate = nn.Sequential(nn.Linear(opt.d_seq_enc_model, opt.d_graph_enc_model, bias=False), nn.Tanh())
    else:
        graph_encoder.activate = nn.Tanh()
    decoder_transformer = DecoderTransformer(opt.layer_attn, device=device)
    decoder = build_decoder(opt, device)
    model = UnifiedModel(opt.training_mode, seq_encoder, graph_encoder, encoder_transformer, decoder, decoder_transformer)
    model.generator = nn.Linear((opt.d_dec_model // opt.maxout_pool_size), opt.tgt_vocab_size, bias=False)
    model.classifier = nn.Sequential(nn.Linear(opt.d_graph_enc_model, 1, bias=False), nn.Sigmoid())
    (model, parameters_cnt) = initialize(model, opt)
    if (checkpoint is not None):
        model.load_state_dict(checkpoint['model'])
        del checkpoint
    model = model.to(device)
    if (len(opt.gpus) > 1):
        model = nn.DataParallel(model, device_ids=opt.gpus)
    return (model, parameters_cnt)
