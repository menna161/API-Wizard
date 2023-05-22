import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

if (__name__ == '__main__'):
    img = cv2.imread('./../docs/output.png')
    print('img: ', img.shape)
    img = np.array(img)
    bbox = np.array([[50, 50, 200, 200]])
    label = np.array(['toan'])
    score = np.array([100])
    (ax, fig) = vis_bbox(img=img, bbox=bbox, label=label, score=score, label_names=label_names)
    fig.savefig('kaka.png')
    fig.show()
    plt.show()
