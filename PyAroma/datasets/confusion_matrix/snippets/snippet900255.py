import numpy as np


def update(self, label_trues, label_preds):
    for (lt, lp) in zip(label_trues, label_preds):
        self.confusion_matrix += self._fast_hist(lt.flatten(), lp.flatten(), self.n_classes)
