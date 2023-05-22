import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from keras.preprocessing.sequence import pad_sequences
import seaborn as sns
import numpy as np
import os
import matplotlib.pyplot as plt
import random
import pickle
import datetime


def extract_dynamic_feature(x):
    global num
    for fea_name in dynamic_context_col:
        mark = False
        if (x[fea_name] == '-1'):
            mark = True
        tmp = x[fea_name].split(' ')[:10]
        if (mark == True):
            x[(fea_name + '_length')] = 0
        else:
            x[(fea_name + '_length')] = len(tmp)
        tmp = np.array(tmp).astype('int')
        x[fea_name] = tmp
    num += 1
    if ((num % 10000) == 0):
        print('processed ID: {}'.format(num))
        end_time = datetime.datetime.now()
        print('time:', (end_time - start_time).seconds)
    return x
