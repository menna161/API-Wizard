import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def vis_bbox(img, bbox, label=None, score=None, instance_colors=None, alpha=1.0, linewidth=2.0, ax=None):
    'Visualize bounding boxes inside the image.\n    Args:\n        img (~numpy.ndarray): An array of shape :math:`(3, height, width)`.\n            This is in RGB format and the range of its value is\n            :math:`[0, 255]`. If this is :obj:`None`, no image is displayed.\n        bbox (~numpy.ndarray): An array of shape :math:`(R, 4)`, where\n            :math:`R` is the number of bounding boxes in the image.\n            Each element is organized\n            by :math:`(y_{min}, x_{min}, y_{max}, x_{max})` in the second axis.\n        label (~numpy.ndarray): An integer array of shape :math:`(R,)`.\n            The values correspond to id for label names stored in\n            :obj:`label_names`. This is optional.\n        score (~numpy.ndarray): A float array of shape :math:`(R,)`.\n             Each value indicates how confident the prediction is.\n             This is optional.\n        label_names (iterable of strings): Name of labels ordered according\n            to label ids. If this is :obj:`None`, labels will be skipped.\n        instance_colors (iterable of tuples): List of colors.\n            Each color is RGB format and the range of its values is\n            :math:`[0, 255]`. The :obj:`i`-th element is the color used\n            to visualize the :obj:`i`-th instance.\n            If :obj:`instance_colors` is :obj:`None`, the red is used for\n            all boxes.\n        alpha (float): The value which determines transparency of the\n            bounding boxes. The range of this value is :math:`[0, 1]`.\n        linewidth (float): The thickness of the edges of the bounding boxes.\n        ax (matplotlib.axes.Axis): The visualization is displayed on this\n            axis. If this is :obj:`None` (default), a new axis is created.\n    Returns:\n        ~matploblib.axes.Axes:\n        Returns the Axes object with the plot for further tweaking.\n    from: https://github.com/chainer/chainercv\n    '
    if ((label is not None) and (not (len(bbox) == len(label)))):
        raise ValueError('The length of label must be same as that of bbox')
    if ((score is not None) and (not (len(bbox) == len(score)))):
        raise ValueError('The length of score must be same as that of bbox')
    if (ax is None):
        fig = plt.figure()
        (h, w, _) = img.shape
        w_ = (w / 60.0)
        h_ = (w_ * (h / w))
        fig.set_size_inches((w_, h_))
        ax = plt.axes([0, 0, 1, 1])
    ax.imshow(img.astype(np.uint8))
    ax.axis('off')
    if (len(bbox) == 0):
        return (fig, ax)
    if (instance_colors is None):
        instance_colors = np.zeros((len(bbox), 3), dtype=np.float32)
        instance_colors[(:, 0)] = 51
        instance_colors[(:, 1)] = 51
        instance_colors[(:, 2)] = 224
    instance_colors = np.array(instance_colors)
    for (i, bb) in enumerate(bbox):
        xy = (bb[0], bb[1])
        height = (bb[3] - bb[1])
        width = (bb[2] - bb[0])
        color = (instance_colors[(i % len(instance_colors))] / 255)
        ax.add_patch(plt.Rectangle(xy, width, height, fill=False, edgecolor=color, linewidth=linewidth, alpha=alpha))
        caption = []
        caption.append(label[i])
        if (len(score) > 0):
            sc = score[i]
            caption.append('{}'.format(sc))
        if (len(caption) > 0):
            face_color = (np.array([225, 51, 123]) / 255)
            ax.text(bb[0], bb[1], ': '.join(caption), fontsize=12, color='black', style='italic', bbox={'facecolor': face_color, 'edgecolor': face_color, 'alpha': 1, 'pad': 0})
    return (fig, ax)
