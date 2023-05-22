import numpy as np


def get_scores(self):
    'Returns accuracy score evaluation result.\n            - overall accuracy\n            - mean accuracy\n            - mean IU\n            - fwavacc\n        '
    hist = self.confusion_matrix
    acc = (np.diag(hist).sum() / hist.sum())
    acc_cls = (np.diag(hist) / hist.sum(axis=1))
    mean_acc_cls = np.nanmean(acc_cls)
    iu = (np.diag(hist) / ((hist.sum(axis=1) + hist.sum(axis=0)) - np.diag(hist)))
    mean_iu = np.nanmean(iu)
    freq = (hist.sum(axis=1) / hist.sum())
    fwavacc = (freq[(freq > 0)] * iu[(freq > 0)]).sum()
    cls_iu = dict(zip(range(self.n_classes), iu))
    return ({'Pixel Acc: ': acc, 'Class Accuracy: ': acc_cls, 'Mean Class Acc: ': mean_acc_cls, 'Freq Weighted IoU: ': fwavacc, 'Mean IoU: ': mean_iu, 'confusion_matrix': self.confusion_matrix}, cls_iu)
