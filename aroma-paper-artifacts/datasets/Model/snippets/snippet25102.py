import os
import code
import tensorflow as tf
from ccn.cfg import get_config
from ccn.vision import Generator, Decoder, Spy, make_symbol_data
from ccn.graph_models import GraphEncoder, GraphDecoder
from ccn.aug import get_noisy_channel
from ccn.graph_data import get_dataset
from ccn.adamlrm import AdamLRM
from ccn.upload import gs_folder_exists


def get_model():
    if (not CFG['JUST_VISION']):
        (ds, node_feature_specs) = get_dataset(**{**CFG, 'num_samples': 1}, test=False)
        CFG['node_feature_specs'] = node_feature_specs
        g_encoder = GraphEncoder(**CFG)
        g_decoder = GraphDecoder(**CFG)
    if CFG['VISION']:
        generator = Generator()
        spy = None
        if CFG['use_spy']:
            spy = Spy()
        decoder = Decoder()
        noisy_channel = get_noisy_channel()
    if CFG['VISION']:
        if CFG['JUST_VISION']:
            print('Using vision model')
            return VisionModel(generator, decoder, noisy_channel, spy)
        else:
            print('Using full model')
            return FullModel(g_encoder, g_decoder, generator, decoder, noisy_channel, spy)
    else:
        print('Using graph model')
        return GraphModel(g_encoder, g_decoder)
