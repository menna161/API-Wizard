from collections import OrderedDict
from fairseq import utils
from fairseq.models import FairseqMultiModel, register_model, register_model_architecture
from fairseq.models.transformer import base_architecture, Embedding, TransformerModel, TransformerEncoder, TransformerDecoder
from fairseq.tasks.multilingual_translation import MultilingualTranslationTask


@classmethod
def build_model(cls, args, task):
    'Build a new model instance.'
    from fairseq.tasks.multilingual_translation import MultilingualTranslationTask
    assert isinstance(task, MultilingualTranslationTask)
    base_multilingual_architecture(args)
    if (not hasattr(args, 'max_source_positions')):
        args.max_source_positions = 1024
    if (not hasattr(args, 'max_target_positions')):
        args.max_target_positions = 1024
    src_langs = [lang_pair.split('-')[0] for lang_pair in task.model_lang_pairs]
    tgt_langs = [lang_pair.split('-')[1] for lang_pair in task.model_lang_pairs]
    if args.share_encoders:
        args.share_encoder_embeddings = True
    if args.share_decoders:
        args.share_decoder_embeddings = True

    def build_embedding(dictionary, embed_dim, path=None):
        num_embeddings = len(dictionary)
        padding_idx = dictionary.pad()
        emb = Embedding(num_embeddings, embed_dim, padding_idx)
        if path:
            embed_dict = utils.parse_embedding(path)
            utils.load_embedding(embed_dict, dictionary, emb)
        return emb
    (shared_encoder_embed_tokens, shared_decoder_embed_tokens) = (None, None)
    if args.share_all_embeddings:
        if (args.encoder_embed_dim != args.decoder_embed_dim):
            raise ValueError('--share-all-embeddings requires --encoder-embed-dim to match --decoder-embed-dim')
        if (args.decoder_embed_path and (args.decoder_embed_path != args.encoder_embed_path)):
            raise ValueError('--share-all-embeddings not compatible with --decoder-embed-path')
        shared_encoder_embed_tokens = FairseqMultiModel.build_shared_embeddings(dicts=task.dicts, langs=task.langs, embed_dim=args.encoder_embed_dim, build_embedding=build_embedding, pretrained_embed_path=args.encoder_embed_path)
        shared_decoder_embed_tokens = shared_encoder_embed_tokens
        args.share_decoder_input_output_embed = True
    else:
        if args.share_encoder_embeddings:
            shared_encoder_embed_tokens = FairseqMultiModel.build_shared_embeddings(dicts=task.dicts, langs=src_langs, embed_dim=args.encoder_embed_dim, build_embedding=build_embedding, pretrained_embed_path=args.encoder_embed_path)
        if args.share_decoder_embeddings:
            shared_decoder_embed_tokens = FairseqMultiModel.build_shared_embeddings(dicts=task.dicts, langs=tgt_langs, embed_dim=args.decoder_embed_dim, build_embedding=build_embedding, pretrained_embed_path=args.decoder_embed_path)
    (lang_encoders, lang_decoders) = ({}, {})

    def get_encoder(lang):
        if (lang not in lang_encoders):
            if (shared_encoder_embed_tokens is not None):
                encoder_embed_tokens = shared_encoder_embed_tokens
            else:
                encoder_embed_tokens = build_embedding(task.dicts[lang], args.encoder_embed_dim, args.encoder_embed_path)
            lang_encoders[lang] = TransformerEncoder(args, task.dicts[lang], encoder_embed_tokens)
        return lang_encoders[lang]

    def get_decoder(lang):
        if (lang not in lang_decoders):
            if (shared_decoder_embed_tokens is not None):
                decoder_embed_tokens = shared_decoder_embed_tokens
            else:
                decoder_embed_tokens = build_embedding(task.dicts[lang], args.decoder_embed_dim, args.decoder_embed_path)
            lang_decoders[lang] = TransformerDecoder(args, task.dicts[lang], decoder_embed_tokens)
        return lang_decoders[lang]
    (shared_encoder, shared_decoder) = (None, None)
    if args.share_encoders:
        shared_encoder = get_encoder(src_langs[0])
    if args.share_decoders:
        shared_decoder = get_decoder(tgt_langs[0])
    (encoders, decoders) = (OrderedDict(), OrderedDict())
    for (lang_pair, src, tgt) in zip(task.model_lang_pairs, src_langs, tgt_langs):
        encoders[lang_pair] = (shared_encoder if (shared_encoder is not None) else get_encoder(src))
        decoders[lang_pair] = (shared_decoder if (shared_decoder is not None) else get_decoder(tgt))
    return MultilingualTransformerModel(encoders, decoders)
