from chainer_bcnn.data import load_image, save_image
from chainer_bcnn.datasets import ImageDataset, VolumeDataset
import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt
import argparse


def test_2d(root):
    filenames = OrderedDict({'image': '{root}/{patient}/slice/*image*.mhd', 'label': '{root}/{patient}/slice/*mask*.mhd', 'mask': '{root}/{patient}/slice/*skin*.mhd'})
    dataset = ImageDataset(root, patients=patient_list, classes=class_list, dtypes=dtypes, filenames=filenames, mask_cvals=mask_cvals)
    print('# dataset:', len(dataset))
    print('# classes:', dataset.n_classes)
    sample = dataset.get_example(0)
    print(sample[0].shape)
    print(sample[1].shape)
    plt.subplot(1, 2, 1)
    plt.imshow(sample[0][(0, :, :)], cmap='gray')
    plt.colorbar()
    plt.subplot(1, 2, 2)
    plt.imshow(sample[1][(:, :)])
    plt.colorbar()
    plt.show()