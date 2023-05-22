from fairseq.models import register_model, register_model_architecture
from fairseq.models.transformer import base_architecture, transformer_wmt_en_de_big, TransformerModel


@classmethod
def build_model(cls, args, task):
    transformer_align(args)
    transformer_model = TransformerModel.build_model(args, task)
    return TransformerAlignModel(transformer_model.encoder, transformer_model.decoder, args)
