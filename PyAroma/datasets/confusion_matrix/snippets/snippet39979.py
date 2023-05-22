import argparse
from pathlib import Path
import numpy as np
import re


def report_scores(confusion_matrix):
    overall_accuracy = (get_overall_accuracy(confusion_matrix) * 100)
    print('Confusion matrix with overall accuracy: {:.2f}%'.format(overall_accuracy))
    print_matrix(confusion_matrix)
    prediction_scores = score_predictions(confusion_matrix)
    print('MIOU: {}'.format(get_mean_intersection_over_union(prediction_scores)))
    for (index, prediction_score) in enumerate(prediction_scores):
        print('Class {:2d} ({:^17}), IOU: {:.4f}'.format(LABELS[index], LABELS_OBJ[LABELS[index]], prediction_score.get_iou()))
    print()
