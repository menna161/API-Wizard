import numpy as np
import os
from gensim.models import KeyedVectors
from keras.layers import add, Bidirectional, Concatenate, CuDNNGRU
from keras.layers import Dense, Embedding, Input, SpatialDropout1D
from keras.models import Model
from keras.optimizers import Adam
from keras.regularizers import l2
from src.BiGRU_experiments.masking import Camouflage, SymmetricMasking
from src.BiGRU_experiments.attension import Attention
from src.BiGRU_experiments.dropout import TimestepDropout
from gensim.downloader import base_dir


def pretrained_embedding():
    '\n    :return: A Model with an embeddings layer\n    '
    inputs = Input(shape=(None,), dtype='int32')
    embeddings = KeyedVectors.load_word2vec_format(EMBEDDINGS_PATH, binary=False)
    word_encodings_weights = np.concatenate((np.zeros((1, embeddings.syn0.shape[(- 1)]), dtype=np.float32), embeddings.syn0), axis=0)
    embeds = Embedding(len(word_encodings_weights), word_encodings_weights.shape[(- 1)], weights=[word_encodings_weights], trainable=False)(inputs)
    return Model(inputs=inputs, outputs=embeds, name='embedding')
