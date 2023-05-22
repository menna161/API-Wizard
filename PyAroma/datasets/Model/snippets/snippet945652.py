from examples.speech_recognition.models.vggtransformer import TransformerDecoder, VGGTransformerEncoder, VGGTransformerModel, vggtransformer_1, vggtransformer_2, vggtransformer_base
from .asr_test_base import DEFAULT_TEST_VOCAB_SIZE, TestFairseqDecoderBase, TestFairseqEncoderBase, TestFairseqEncoderDecoderModelBase, get_dummy_dictionary, get_dummy_encoder_output, get_dummy_input


def setUp(self):

    def override_config(args):
        '\n            vggtrasformer_2 use 16 layers of transformer,\n            for testing purpose, it is too expensive. For fast turn-around\n            test, reduce the number of layers to 3.\n            '
        args.transformer_enc_config = '((1024, 16, 4096, True, 0.15, 0.15, 0.15),) * 3'
    super().setUp()
    extra_args_setter = [vggtransformer_2, override_config]
    self.setUpModel(VGGTransformerModel, extra_args_setter)
    self.setUpInput(get_dummy_input(T=50, D=80, B=5, K=DEFAULT_TEST_VOCAB_SIZE))
