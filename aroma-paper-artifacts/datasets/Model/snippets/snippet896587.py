from fairseq import options, utils
from fairseq.models import FairseqLanguageModel, register_model, register_model_architecture
from fairseq.models.transformer import Embedding, TransformerDecoder
from fairseq.modules import AdaptiveInput, CharacterTokenEmbedder


@classmethod
def build_model(cls, args, task):
    'Build a new model instance.'
    base_lm_architecture(args)
    if (getattr(args, 'max_target_positions', None) is None):
        args.max_target_positions = getattr(args, 'tokens_per_sample', DEFAULT_MAX_TARGET_POSITIONS)
    if args.character_embeddings:
        embed_tokens = CharacterTokenEmbedder(task.source_dictionary, eval(args.character_filters), args.character_embedding_dim, args.decoder_embed_dim, args.char_embedder_highway_layers)
    elif args.adaptive_input:
        embed_tokens = AdaptiveInput(len(task.source_dictionary), task.source_dictionary.pad(), args.decoder_input_dim, args.adaptive_input_factor, args.decoder_embed_dim, options.eval_str_list(args.adaptive_input_cutoff, type=int))
    else:
        embed_tokens = Embedding(len(task.source_dictionary), args.decoder_input_dim, task.source_dictionary.pad())
    if args.tie_adaptive_weights:
        assert args.adaptive_input
        assert (args.adaptive_input_factor == args.adaptive_softmax_factor)
        assert (args.adaptive_softmax_cutoff == args.adaptive_input_cutoff), '{} != {}'.format(args.adaptive_softmax_cutoff, args.adaptive_input_cutoff)
        assert (args.decoder_input_dim == args.decoder_output_dim)
    decoder = TransformerDecoder(args, task.target_dictionary, embed_tokens, no_encoder_attn=True)
    return TransformerLanguageModel(decoder)
