import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import numpy as np
import cv2


def draw_stitched_boxes(im, data, outpath):
    (fig, ax) = plt.subplots(1)
    data = data[data[(:, 4)].argsort()]
    ax.imshow(im)
    (width, height, channels) = im.shape
    heatmap = np.zeros([width, height])
    for box in data:
        heatmap[(int(box[1]):int(box[3]), int(box[0]):int(box[2]))] = box[4]
    heatmap[(0:1, 0:1)] = 1
    heatmap[(0:1, 1:2)] = 0
    plt.imshow(heatmap, alpha=0.4, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.title('Stitching visualization')
    plt.show()
    plt.savefig(outpath, dpi=600)
    plt.close()
