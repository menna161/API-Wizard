import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import numpy as np
import cv2


def draw_boxes(args, im, recognized_boxes, recognized_scores, boxes, confs, scale, img_id):
    path = os.path.join('eval', args.exp_name, (img_id + '.png'))
    if (not os.path.exists(os.path.dirname(path))):
        os.makedirs(os.path.dirname(path))
    (fig, ax) = plt.subplots(1)
    scale = scale.cpu().numpy()
    ax.imshow(im)
    (width, height, channels) = im.shape
    heatmap = np.zeros([width, height])
    if ((len(recognized_scores) > 1) and (len(recognized_boxes) > 1)):
        data = np.concatenate((recognized_boxes, np.transpose([recognized_scores])), axis=1)
        data = data[data[(:, 4)].argsort()]
        for box in data:
            heatmap[(int(box[1]):int(box[3]), int(box[0]):int(box[2]))] = box[4]
        for box in recognized_boxes:
            rect = patches.Rectangle((box[0], box[1]), (box[2] - box[0]), (box[3] - box[1]), linewidth=1, edgecolor='g', facecolor='none')
            ax.add_patch(rect)
    heatmap[(0:1, 0:1)] = 1
    heatmap[(0:1, 1:2)] = 0
    plt.imshow(heatmap, alpha=0.4, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.title(args.exp_name)
    plt.show()
    plt.savefig(path, dpi=600)
    plt.close()
