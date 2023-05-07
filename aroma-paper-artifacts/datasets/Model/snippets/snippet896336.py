from fairseq import options
from fairseq.models import FairseqLanguageModel, register_model, register_model_architecture
from fairseq.models.fconv import FConvDecoder


@classmethod
def build_model(cls, args, task):
    'Build a new model instance.'
    base_lm_architecture(args)
    if (hasattr(args, 'max_target_positions') and (not hasattr(args, 'tokens_per_sample'))):
        args.tokens_per_sample = args.max_target_positions
    decoder = FConvDecoder(dictionary=task.target_dictionary, embed_dim=args.decoder_embed_dim, convolutions=eval(args.decoder_layers), out_embed_dim=args.decoder_embed_dim, attention=eval(args.decoder_attention), dropout=args.dropout, max_positions=args.tokens_per_sample, share_embed=False, positional_embeddings=False, adaptive_softmax_cutoff=(options.eval_str_list(args.adaptive_softmax_cutoff, type=int) if (args.criterion == 'adaptive_loss') else None), adaptive_softmax_dropout=args.adaptive_softmax_dropout)
    return FConvLanguageModel(decoder)
