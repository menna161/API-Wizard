import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from fairseq import utils
from fairseq.models import FairseqEncoder, FairseqIncrementalDecoder, FairseqEncoderDecoderModel, register_model, register_model_architecture
from fairseq.modules import AdaptiveSoftmax, BeamableMM, GradMultiply, LearnedPositionalEmbedding, LinearizedConvolution
from fairseq.modules import ConvTBC


@classmethod
def build_model(cls, args, task):
    'Build a new model instance.'
    base_architecture(args)
    encoder_embed_dict = None
    if args.encoder_embed_path:
        encoder_embed_dict = utils.parse_embedding(args.encoder_embed_path)
        utils.print_embed_overlap(encoder_embed_dict, task.source_dictionary)
    decoder_embed_dict = None
    if args.decoder_embed_path:
        decoder_embed_dict = utils.parse_embedding(args.decoder_embed_path)
        utils.print_embed_overlap(decoder_embed_dict, task.target_dictionary)
    encoder = FConvEncoder(dictionary=task.source_dictionary, embed_dim=args.encoder_embed_dim, embed_dict=encoder_embed_dict, convolutions=eval(args.encoder_layers), dropout=args.dropout, max_positions=args.max_source_positions)
    decoder = FConvDecoder(dictionary=task.target_dictionary, embed_dim=args.decoder_embed_dim, embed_dict=decoder_embed_dict, convolutions=eval(args.decoder_layers), out_embed_dim=args.decoder_out_embed_dim, attention=eval(args.decoder_attention), dropout=args.dropout, max_positions=args.max_target_positions, share_embed=args.share_input_output_embed)
    return FConvModel(encoder, decoder)
