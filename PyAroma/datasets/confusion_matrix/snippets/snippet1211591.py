import os
import time
import numpy as np
import torch
from PIL import Image
from datasets.cityscapes_Dataset import name_classes


def Print_Every_class_Eval(self, out_16_13=False):
    MIoU = (np.diag(self.confusion_matrix) / ((np.sum(self.confusion_matrix, axis=1) + np.sum(self.confusion_matrix, axis=0)) - np.diag(self.confusion_matrix)))
    MPA = (np.diag(self.confusion_matrix) / self.confusion_matrix.sum(axis=1))
    Precision = (np.diag(self.confusion_matrix) / self.confusion_matrix.sum(axis=0))
    Class_ratio = (np.sum(self.confusion_matrix, axis=1) / np.sum(self.confusion_matrix))
    Pred_retio = (np.sum(self.confusion_matrix, axis=0) / np.sum(self.confusion_matrix))
    print(((((('===>Everyclass:\t' + 'MPA\t') + 'MIoU\t') + 'PC\t') + 'Ratio\t') + 'Pred_Retio'))
    if out_16_13:
        MIoU = MIoU[synthia_set_16]
    for ind_class in range(len(MIoU)):
        pa = (str(round((MPA[ind_class] * 100), 2)) if (not np.isnan(MPA[ind_class])) else 'nan')
        iou = (str(round((MIoU[ind_class] * 100), 2)) if (not np.isnan(MIoU[ind_class])) else 'nan')
        pc = (str(round((Precision[ind_class] * 100), 2)) if (not np.isnan(Precision[ind_class])) else 'nan')
        cr = (str(round((Class_ratio[ind_class] * 100), 2)) if (not np.isnan(Class_ratio[ind_class])) else 'nan')
        pr = (str(round((Pred_retio[ind_class] * 100), 2)) if (not np.isnan(Pred_retio[ind_class])) else 'nan')
        print(((((((((((('===>' + name_classes[ind_class]) + ':\t') + pa) + '\t') + iou) + '\t') + pc) + '\t') + cr) + '\t') + pr))
