import os
import time
import numpy as np
import torch
from PIL import Image
from datasets.cityscapes_Dataset import name_classes


def Mean_Intersection_over_Union(self, out_16_13=False):
    MIoU = (np.diag(self.confusion_matrix) / ((np.sum(self.confusion_matrix, axis=1) + np.sum(self.confusion_matrix, axis=0)) - np.diag(self.confusion_matrix)))
    if self.synthia:
        MIoU_16 = np.nanmean(MIoU[:self.ignore_index])
        MIoU_13 = np.nanmean(MIoU[synthia_set_16_to_13])
        return (MIoU_16, MIoU_13)
    if out_16_13:
        MIoU_16 = np.nanmean(MIoU[synthia_set_16])
        MIoU_13 = np.nanmean(MIoU[synthia_set_13])
        return (MIoU_16, MIoU_13)
    MIoU = np.nanmean(MIoU[:self.ignore_index])
    return MIoU
