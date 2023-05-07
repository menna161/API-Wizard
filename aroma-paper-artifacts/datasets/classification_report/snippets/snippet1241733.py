import torch
from tqdm import tqdm
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score, classification_report


def value(self):
    '\n        计算指标得分\n        '
    score = classification_report(y_true=self.y_true, y_pred=self.y_pred, target_names=self.target_names)
    print(f'''

 classification report: {score}''')
