from fairseq import options
from fairseq.models import FairseqLanguageModel, register_model, register_model_architecture
from fairseq.models.lightconv import Embedding, LightConvDecoder
from fairseq.modules import AdaptiveInput, CharacterTokenEmbedder


@classmethod
def build_model(cls, args, task):
    'Build a new model instance.'
    base_lm_architecture(args)
    if (not hasattr(args, 'max_source_positions')):
        args.max_source_positions = args.tokens_per_sample
    if (not hasattr(args, 'max_target_positions')):
        args.max_target_positions = args.tokens_per_sample
    if args.character_embeddings:
        embed_tokens = CharacterTokenEmbedder(task.dictionary, eval(args.character_filters), args.character_embedding_dim, args.decoder_embed_dim, args.char_embedder_highway_layers)
    elif args.adaptive_input:
        embed_tokens = AdaptiveInput(len(task.dictionary), task.dictionary.pad(), args.decoder_input_dim, args.adaptive_input_factor, args.decoder_embed_dim, options.eval_str_list(args.adaptive_input_cutoff, type=int))
    else:
        embed_tokens = Embedding(len(task.dictionary), args.decoder_input_dim, task.dictionary.pad())
    if args.tie_adaptive_weights:
        assert args.adaptive_input
        assert (args.adaptive_input_factor == args.adaptive_softmax_factor)
        assert (args.adaptive_softmax_cutoff == args.adaptive_input_cutoff), '{} != {}'.format(args.adaptive_softmax_cutoff, args.adaptive_input_cutoff)
        assert (args.decoder_input_dim == args.decoder_output_dim)
    decoder = LightConvDecoder(args, task.output_dictionary, embed_tokens, no_encoder_attn=True, final_norm=False)
    return LightConvLanguageModel(decoder)
