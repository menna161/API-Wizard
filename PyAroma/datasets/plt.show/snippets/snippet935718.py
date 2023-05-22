from collections import Sequence
import matplotlib.pyplot as plt
import mmcv
import numpy as np
import torch


def show_ann(coco, img, ann_info):
    plt.imshow(mmcv.bgr2rgb(img))
    plt.axis('off')
    coco.showAnns(ann_info)
    plt.show()
