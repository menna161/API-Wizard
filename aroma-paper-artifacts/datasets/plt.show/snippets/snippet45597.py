import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import numpy as np
import cv2


def draw_all_boxes(im, data, recognized_boxes, gt_boxes, outpath):
    if (len(data) == 0):
        return
    (fig, ax) = plt.subplots(1)
    data = data[data[(:, 4)].argsort()]
    ax.imshow(im)
    (width, height, channels) = im.shape
    heatmap = np.zeros([width, height])
    if (data is not None):
        for box in data:
            heatmap[(int(box[1]):int(box[3]), int(box[0]):int(box[2]))] = box[4]
    if (recognized_boxes is not None):
        for box in recognized_boxes:
            rect = patches.Rectangle((box[0], box[1]), (box[2] - box[0]), (box[3] - box[1]), linewidth=1, edgecolor='g', facecolor='none')
            ax.add_patch(rect)
    if (gt_boxes is not None):
        for box in gt_boxes:
            rect = patches.Rectangle((box[0], box[1]), (box[2] - box[0]), (box[3] - box[1]), linewidth=0.25, edgecolor='b', facecolor='none')
            ax.add_patch(rect)
    heatmap[(0:1, 0:1)] = 1
    heatmap[(0:1, 1:2)] = 0
    plt.imshow(heatmap, alpha=0.4, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.title('Stitching visualization')
    plt.show()
    plt.savefig(outpath, dpi=600)
    plt.close()
