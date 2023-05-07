import os
import time
import tensorflow as tf
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from . import config as cfg
from . import datasets
from . import utils
from . import models


@tf.function
def train_step(inp, targ, targ_lang_tokenizer, enc_hidden, encoder, decoder, optimizer):
    loss = 0
    with tf.GradientTape() as tape:
        (enc_output, enc_hidden) = encoder(inp, enc_hidden)
        dec_hidden = enc_hidden
        dec_input = tf.expand_dims(([targ_lang_tokenizer.word_index['<start>']] * cfg.BATCH_SIZE), 1)
        for t in range(1, targ.shape[1]):
            (predictions, dec_hidden, _) = decoder(dec_input, dec_hidden, enc_output)
            loss += loss_function(targ[(:, t)], predictions)
            dec_input = tf.expand_dims(targ[(:, t)], 1)
    batch_loss = (loss / int(targ.shape[1]))
    variables = (encoder.trainable_variables + decoder.trainable_variables)
    gradients = tape.gradient(loss, variables)
    optimizer.apply_gradients(zip(gradients, variables))
    return batch_loss
