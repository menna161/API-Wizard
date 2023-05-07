import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from fairseq import options, utils
from fairseq.models import FairseqEncoder, FairseqIncrementalDecoder, FairseqEncoderDecoderModel, register_model, register_model_architecture
from fairseq.modules import AdaptiveSoftmax, DynamicConv, LayerNorm, PositionalEmbedding, LightweightConv, MultiheadAttention


@classmethod
def build_model(cls, args, task):
    'Build a new model instance.'
    base_architecture(args)
    if (not hasattr(args, 'max_source_positions')):
        args.max_source_positions = 1024
    if (not hasattr(args, 'max_target_positions')):
        args.max_target_positions = 1024
    (src_dict, tgt_dict) = (task.source_dictionary, task.target_dictionary)

    def build_embedding(dictionary, embed_dim, path=None):
        num_embeddings = len(dictionary)
        padding_idx = dictionary.pad()
        emb = Embedding(num_embeddings, embed_dim, padding_idx)
        if path:
            embed_dict = utils.parse_embedding(path)
            utils.load_embedding(embed_dict, dictionary, emb)
        return emb
    if args.share_all_embeddings:
        if (src_dict != tgt_dict):
            raise RuntimeError('--share-all-embeddings requires a joined dictionary')
        if (args.encoder_embed_dim != args.decoder_embed_dim):
            raise RuntimeError('--share-all-embeddings requires --encoder-embed-dim to match --decoder-embed-dim')
        if (args.decoder_embed_path and (args.decoder_embed_path != args.encoder_embed_path)):
            raise RuntimeError('--share-all-embeddings not compatible with --decoder-embed-path')
        encoder_embed_tokens = build_embedding(src_dict, args.encoder_embed_dim, args.encoder_embed_path)
        decoder_embed_tokens = encoder_embed_tokens
        args.share_decoder_input_output_embed = True
    else:
        encoder_embed_tokens = build_embedding(src_dict, args.encoder_embed_dim, args.encoder_embed_path)
        decoder_embed_tokens = build_embedding(tgt_dict, args.decoder_embed_dim, args.decoder_embed_path)
    encoder = LightConvEncoder(args, src_dict, encoder_embed_tokens)
    decoder = LightConvDecoder(args, tgt_dict, decoder_embed_tokens)
    return LightConvModel(encoder, decoder)
