import os
import time
import numpy as np
import torch
from PIL import Image
from datasets.cityscapes_Dataset import name_classes


def Mean_Pixel_Accuracy(self, out_16_13=False):
    MPA = (np.diag(self.confusion_matrix) / self.confusion_matrix.sum(axis=1))
    if self.synthia:
        MPA_16 = np.nanmean(MPA[:self.ignore_index])
        MPA_13 = np.nanmean(MPA[synthia_set_16_to_13])
        return (MPA_16, MPA_13)
    if out_16_13:
        MPA_16 = np.nanmean(MPA[synthia_set_16])
        MPA_13 = np.nanmean(MPA[synthia_set_13])
        return (MPA_16, MPA_13)
    MPA = np.nanmean(MPA[:self.ignore_index])
    return MPA
