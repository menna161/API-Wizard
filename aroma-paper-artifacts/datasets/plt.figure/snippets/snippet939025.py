import matplotlib.pyplot as plt
import numpy as np
import torch
from mpl_toolkits.mplot3d import Axes3D


def get_ptcloud_img(ptcloud):
    fig = plt.figure(figsize=(8, 8))
    (x, z, y) = ptcloud.transpose(1, 0)
    ax = fig.gca(projection=Axes3D.name, adjustable='box')
    ax.axis('off')
    ax.axis('scaled')
    ax.view_init(30, 45)
    (max, min) = (np.max(ptcloud), np.min(ptcloud))
    ax.set_xbound(min, max)
    ax.set_ybound(min, max)
    ax.set_zbound(min, max)
    ax.scatter(x, y, z, zdir='z', c=x, cmap='jet')
    fig.canvas.draw()
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img = img.reshape((fig.canvas.get_width_height()[::(- 1)] + (3,)))
    return img
