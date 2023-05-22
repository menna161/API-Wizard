import torch
from tqdm import tqdm
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score, classification_report


def value(self):
    '\n        计算指标得分\n        '
    for (i, label) in self.id2label.items():
        auc = roc_auc_score(y_score=self.y_prob[(:, i)], y_true=self.y_true[(:, i)])
        print(f'label:{label} - auc: {auc:.4f}')
