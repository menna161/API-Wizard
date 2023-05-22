import os
import re
import gc
import sys
import json
import codecs
import datetime
import warnings
import numpy as np
import pandas as pd
import tensorflow as tf
from tqdm import tqdm
from random import choice
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.metrics import f1_score
from sklearn.model_selection import KFold
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
import keras.backend as K
from keras.layers import *
from keras.callbacks import *
from keras.models import Model
from keras.optimizers import Adam
from keras.utils import to_categorical
from keras.metrics import top_k_categorical_accuracy, categorical_accuracy
from keras_bert import load_trained_model_from_checkpoint, Tokenizer
from keras.callbacks import Callback
from sklearn.metrics import f1_score, accuracy_score


def run_cv(nfolds, data, data_label, data_test, epochs=10, date_str='1107'):
    skf = StratifiedKFold(n_splits=nfolds, shuffle=True, random_state=214683).split(data, train['label'])
    train_model_pred = np.zeros((len(data), 2))
    test_model_pred = np.zeros((len(data_test), 2))
    for (i, (train_fold, test_fold)) in enumerate(skf):
        print('Fold: ', (i + 1))
        '数据部分'
        (X_train, X_valid) = (data[train_fold, :], data[test_fold, :])
        train_D = data_generator(X_train, shuffle=True)
        valid_D = data_generator(X_valid, shuffle=False)
        test_D = data_generator(data_test, shuffle=False)
        time_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        '模型部分'
        model = build_bert(2)
        early_stopping = EarlyStopping(monitor='val_f1_metric', patience=3)
        plateau = ReduceLROnPlateau(monitor='val_f1_metric', verbose=1, mode='max', factor=0.5, patience=1)
        checkpoint = ModelCheckpoint(((('./models/keras_model/fusai' + date_str) + str(i)) + '.hdf5'), monitor='val_f1_metric', verbose=2, save_best_only=True, mode='max', save_weights_only=True)
        model.fit_generator(train_D.__iter__(), steps_per_epoch=len(train_D), epochs=epochs, validation_data=valid_D.__iter__(), validation_steps=len(valid_D), callbacks=[early_stopping, plateau, checkpoint], verbose=2)
        model.load_weights(((('./models/keras_model/fusai' + date_str) + str(i)) + '.hdf5'))
        val = model.predict_generator(valid_D.__iter__(), steps=len(valid_D), verbose=0)
        print(val)
        score = f1_score(train['label'].values[test_fold], np.argmax(val, axis=1))
        global f1
        f1.append(score)
        print('validate {} f1_score:{}'.format((i + 1), score))
        train_model_pred[test_fold, :] = val
        test_model_pred += model.predict_generator(test_D.__iter__(), steps=len(test_D), verbose=0)
        del model
        gc.collect()
        K.clear_session()
    return (train_model_pred, test_model_pred)
