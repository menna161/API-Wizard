import re
import torch
import torch.nn as nn
from torch.nn.init import xavier_uniform_
import onmt.inputters as inputters
import onmt.modules
from onmt.encoders import str2enc
from onmt.decoders import str2dec
from onmt.modules import Embeddings, VecEmbedding, CopyGenerator
from onmt.modules.util_class import Cast
from onmt.utils.misc import use_gpu
from onmt.utils.logging import logger
from onmt.utils.parse import ArgumentParser


def build_base_model(model_opt, fields, gpu, checkpoint=None, gpu_id=None):
    "Build a model from opts.\n\n    Args:\n        model_opt: the option loaded from checkpoint. It's important that\n            the opts have been updated and validated. See\n            :class:`onmt.utils.parse.ArgumentParser`.\n        fields (dict[str, torchtext.data.Field]):\n            `Field` objects for the model.\n        gpu (bool): whether to use gpu.\n        checkpoint: the model gnerated by train phase, or a resumed snapshot\n                    model from a stopped training.\n        gpu_id (int or NoneType): Which GPU to use.\n\n    Returns:\n        the NMTModel.\n    "
    try:
        model_opt.attention_dropout
    except AttributeError:
        model_opt.attention_dropout = model_opt.dropout
    if ((model_opt.model_type == 'text') or (model_opt.model_type == 'vec')):
        src_field = fields['src']
        src_emb = build_embeddings(model_opt, src_field)
    else:
        src_emb = None
    encoder = build_encoder(model_opt, src_emb)
    tgt_field = fields['tgt']
    tgt_emb = build_embeddings(model_opt, tgt_field, for_encoder=False)
    if model_opt.share_embeddings:
        assert (src_field.base_field.vocab == tgt_field.base_field.vocab), 'preprocess with -share_vocab if you use share_embeddings'
        tgt_emb.word_lut.weight = src_emb.word_lut.weight
    decoder = build_decoder(model_opt, tgt_emb)
    if (gpu and (gpu_id is not None)):
        device = torch.device('cuda', gpu_id)
    elif (gpu and (not gpu_id)):
        device = torch.device('cuda')
    elif (not gpu):
        device = torch.device('cpu')
    model = onmt.models.NMTModel(encoder, decoder)
    if (not model_opt.copy_attn):
        if (model_opt.generator_function == 'sparsemax'):
            gen_func = onmt.modules.sparse_activations.LogSparsemax(dim=(- 1))
        else:
            gen_func = nn.LogSoftmax(dim=(- 1))
        generator = nn.Sequential(nn.Linear(model_opt.dec_rnn_size, len(fields['tgt'].base_field.vocab)), Cast(torch.float32), gen_func)
        if model_opt.share_decoder_embeddings:
            generator[0].weight = decoder.embeddings.word_lut.weight
    else:
        tgt_base_field = fields['tgt'].base_field
        vocab_size = len(tgt_base_field.vocab)
        pad_idx = tgt_base_field.vocab.stoi[tgt_base_field.pad_token]
        generator = CopyGenerator(model_opt.dec_rnn_size, vocab_size, pad_idx)
        if model_opt.share_decoder_embeddings:
            generator.linear.weight = decoder.embeddings.word_lut.weight
    if (checkpoint is not None):

        def fix_key(s):
            s = re.sub('(.*)\\.layer_norm((_\\d+)?)\\.b_2', '\\1.layer_norm\\2.bias', s)
            s = re.sub('(.*)\\.layer_norm((_\\d+)?)\\.a_2', '\\1.layer_norm\\2.weight', s)
            return s
        checkpoint['model'] = {fix_key(k): v for (k, v) in checkpoint['model'].items()}
        model.load_state_dict(checkpoint['model'], strict=False)
        generator.load_state_dict(checkpoint['generator'], strict=False)
    else:
        if (model_opt.param_init != 0.0):
            for p in model.parameters():
                p.data.uniform_((- model_opt.param_init), model_opt.param_init)
            for p in generator.parameters():
                p.data.uniform_((- model_opt.param_init), model_opt.param_init)
        if model_opt.param_init_glorot:
            for p in model.parameters():
                if (p.dim() > 1):
                    xavier_uniform_(p)
            for p in generator.parameters():
                if (p.dim() > 1):
                    xavier_uniform_(p)
        if hasattr(model.encoder, 'embeddings'):
            model.encoder.embeddings.load_pretrained_vectors(model_opt.pre_word_vecs_enc)
        if hasattr(model.decoder, 'embeddings'):
            model.decoder.embeddings.load_pretrained_vectors(model_opt.pre_word_vecs_dec)
    model.generator = generator
    model.to(device)
    if ((model_opt.model_dtype == 'fp16') and (model_opt.optim == 'fusedadam')):
        model.half()
    return model
