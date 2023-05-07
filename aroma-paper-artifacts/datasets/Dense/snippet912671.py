import tensorflow_hub as hub
import tensorflow as tf
import keras.backend.tensorflow_backend as K
import numpy as np
import random
from keras.layers import Layer, Input, Dense, Dropout, Concatenate
from keras.losses import mean_squared_error
from keras.models import Model
from keras.optimizers import Adam


def compile_bert(shape, dropout_rate, lr, mode, human_metric):
    "\n    Using the above class, creates, compiles the and returns the BERT model ready to be trained\n    :param shape: The Input shape (We used 512 as the max bpes that can be fit).\n    :param dropout_rate: The dropout rate of the model.\n    :param lr: The learning rate of the model.\n    :param mode: Depending on your choice : ['Single Task', 'Multi Task-1', 'Multi Task-5'].\n    :param human_metric: The metric for which the model will be trained at.\n    :return: The compiler model ready to be used.\n    "
    random.seed(11)
    np.random.seed(13)
    tf.set_random_seed(21)
    word_inputs = Input(shape=(shape[1],), name='word_inputs', dtype='int32')
    mask_inputs = Input(shape=(shape[1],), name='pos_inputs', dtype='int32')
    seg_inputs = Input(shape=(shape[1],), name='seg_inputs', dtype='int32')
    doc_encoding = BERT()([word_inputs, mask_inputs, seg_inputs])
    doc_encoding = Dropout(dropout_rate)(doc_encoding)
    model = None
    if (mode == 'Single Task'):
        outputs = Dense(1, activation='linear', name='outputs')(doc_encoding)
        model = Model(inputs=[word_inputs, mask_inputs, seg_inputs], outputs=[outputs])
    elif (mode == 'Multi Task-1'):
        outputs = Dense(5, activation='linear', name='outputs')(doc_encoding)
        model = Model(inputs=[word_inputs, mask_inputs, seg_inputs], outputs=[outputs])
    elif (mode == 'Multi Task-5'):
        output_q1 = Dense(1, activation='linear', name='output_Q1')(doc_encoding)
        output_q2 = Dense(1, activation='linear', name='output_Q2')(doc_encoding)
        output_q3 = Dense(1, activation='linear', name='output_Q3')(doc_encoding)
        output_q4 = Dense(1, activation='linear', name='output_Q4')(doc_encoding)
        output_q5 = Dense(1, activation='linear', name='output_Q5')(doc_encoding)
        model = Model(inputs=[word_inputs, mask_inputs, seg_inputs], outputs=[Concatenate()([output_q1, output_q2, output_q3, output_q4, output_q5])])
    set_quality_index(mode=mode, quality=human_metric)
    model.compile(optimizer=Adam(lr=lr), loss='mse', loss_weights=None, metrics=[custom_loss])
    return model
