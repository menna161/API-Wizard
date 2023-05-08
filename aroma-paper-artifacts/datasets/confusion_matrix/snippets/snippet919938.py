from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from argparse import ArgumentParser
from model import *
import tensorflow as tf
import numpy as np
from helper import showClassTable, maybeExtract
import os
from tqdm import tqdm


def test(t_data, t_label, test_iterations=1, evalate=False):
    assert (test_data.shape[0] == test_label.shape[0])
    y_predict_class = model['predict_class_number']
    (overAllAcc, avgAcc, averageAccClass) = ([], [], [])
    for _ in range(test_iterations):
        pred_class = []
        for t in tqdm(t_data):
            t = np.expand_dims(t, axis=0)
            feed_dict_test = {img_entry: t, prob: 1.0}
            prediction = session.run(y_predict_class, feed_dict=feed_dict_test)
            pred_class.append(prediction)
        true_class = np.argmax(t_label, axis=1)
        conMatrix = confusion_matrix(true_class, pred_class)
        classArray = []
        for c in range(len(conMatrix)):
            recallScore = (conMatrix[c][c] / sum(conMatrix[c]))
            classArray += [recallScore]
        averageAccClass.append(classArray)
        avgAcc.append((sum(classArray) / len(classArray)))
        overAllAcc.append(accuracy_score(true_class, pred_class))
    averageAccClass = np.transpose(averageAccClass)
    meanPerClass = np.mean(averageAccClass, axis=1)
    showClassTable(meanPerClass, title='Class accuracy')
    print(('Average Accuracy: ' + str(np.mean(avgAcc))))
    print(('Overall Accuracy: ' + str(np.mean(overAllAcc))))
