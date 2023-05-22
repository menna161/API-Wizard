import os
import json
import numpy as np
from sklearn.model_selection import train_test_split
import re


def split_train_dev_test():
    f = open('wos_total.json', 'r')
    data = f.readlines()
    f.close()
    id = [i for i in range(46985)]
    np_data = np.array(data)
    np.random.shuffle(id)
    np_data = np_data[id]
    (train, test) = train_test_split(np_data, test_size=0.2, random_state=0)
    (train, val) = train_test_split(train, test_size=0.2, random_state=0)
    train = list(train)
    val = list(val)
    test = list(test)
    f = open('wos_train.json', 'w')
    f.writelines(train)
    f.close()
    f = open('wos_test.json', 'w')
    f.writelines(test)
    f.close()
    f = open('wos_val.json', 'w')
    f.writelines(val)
    f.close()
    print(len(train), len(val), len(test))
    return
