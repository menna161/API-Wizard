import os
import time
import numpy as np
import torch
from PIL import Image
from datasets.cityscapes_Dataset import name_classes


def Mean_Precision(self, out_16_13=False):
    Precision = (np.diag(self.confusion_matrix) / self.confusion_matrix.sum(axis=0))
    if self.synthia:
        Precision_16 = np.nanmean(Precision[:self.ignore_index])
        Precision_13 = np.nanmean(Precision[synthia_set_16_to_13])
        return (Precision_16, Precision_13)
    if out_16_13:
        Precision_16 = np.nanmean(Precision[synthia_set_16])
        Precision_13 = np.nanmean(Precision[synthia_set_13])
        return (Precision_16, Precision_13)
    Precision = np.nanmean(Precision[:self.ignore_index])
    return Precision
