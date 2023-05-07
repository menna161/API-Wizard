import math
import numpy as np
import os
import SimpleITK as sitk
import time
import functions.kernel.conv_kernel as conv_kernel
import functions.tf_utils as tfu
import tensorflow as tf
import tensorflow as tf
import tensorflow as tf
import matplotlib.pyplot as plt


def SITKshow(img, title=None, margin=0.05, dpi=80):
    import matplotlib.pyplot as plt
    nda = sitk.GetArrayViewFromImage(img)
    spacing = img.GetSpacing()
    ysize = nda.shape[0]
    xsize = nda.shape[1]
    figsize = ((((1 + margin) * ysize) / dpi), (((1 + margin) * xsize) / dpi))
    fig = plt.figure(title, figsize=figsize, dpi=dpi)
    ax = fig.add_axes([margin, margin, (1 - (2 * margin)), (1 - (2 * margin))])
    extent = (0, (xsize * spacing[1]), 0, (ysize * spacing[0]))
    t = ax.imshow(nda, extent=extent, interpolation='hamming', cmap='gray', origin='lower')
    if title:
        plt.title(title)
