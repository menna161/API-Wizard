import os
import time
import numpy as np
import torch
from PIL import Image
from datasets.cityscapes_Dataset import name_classes


def Frequency_Weighted_Intersection_over_Union(self, out_16_13=False):
    FWIoU = np.multiply(np.sum(self.confusion_matrix, axis=1), np.diag(self.confusion_matrix))
    FWIoU = (FWIoU / ((np.sum(self.confusion_matrix, axis=1) + np.sum(self.confusion_matrix, axis=0)) - np.diag(self.confusion_matrix)))
    if self.synthia:
        FWIoU_16 = (np.sum((i for i in FWIoU if (not np.isnan(i)))) / np.sum(self.confusion_matrix))
        FWIoU_13 = (np.sum((i for i in FWIoU[synthia_set_16_to_13] if (not np.isnan(i)))) / np.sum(self.confusion_matrix))
        return (FWIoU_16, FWIoU_13)
    if out_16_13:
        FWIoU_16 = (np.sum((i for i in FWIoU[synthia_set_16] if (not np.isnan(i)))) / np.sum(self.confusion_matrix))
        FWIoU_13 = (np.sum((i for i in FWIoU[synthia_set_13] if (not np.isnan(i)))) / np.sum(self.confusion_matrix))
        return (FWIoU_16, FWIoU_13)
    FWIoU = (np.sum((i for i in FWIoU if (not np.isnan(i)))) / np.sum(self.confusion_matrix))
    return FWIoU
