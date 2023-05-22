import torch
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from models import EfficientDet
from torchvision import transforms
import numpy as np
import skimage
from datasets import get_augumentation, VOC_CLASSES
from timeit import default_timer as timer
import argparse
import copy
from utils import vis_bbox, EFFICIENTDET


def process(self, file_name=None, img=None, show=False):
    if (file_name is not None):
        img = cv2.imread(file_name)
    origin_img = copy.deepcopy(img)
    augmentation = self.transform(image=img)
    img = augmentation['image']
    img = img.to(self.device)
    img = img.unsqueeze(0)
    with torch.no_grad():
        (scores, classification, transformed_anchors) = self.model(img)
        bboxes = list()
        labels = list()
        bbox_scores = list()
        colors = list()
        for j in range(scores.shape[0]):
            bbox = transformed_anchors[([j], :)][0].data.cpu().numpy()
            x1 = int(((bbox[0] * origin_img.shape[1]) / self.size_image[1]))
            y1 = int(((bbox[1] * origin_img.shape[0]) / self.size_image[0]))
            x2 = int(((bbox[2] * origin_img.shape[1]) / self.size_image[1]))
            y2 = int(((bbox[3] * origin_img.shape[0]) / self.size_image[0]))
            bboxes.append([x1, y1, x2, y2])
            label_name = VOC_CLASSES[int(classification[[j]])]
            labels.append(label_name)
            if args.cam:
                cv2.rectangle(origin_img, (x1, y1), (x2, y2), (179, 255, 179), 2, 1)
            if args.score:
                score = (np.around(scores[[j]].cpu().numpy(), decimals=2) * 100)
                if args.cam:
                    (labelSize, baseLine) = cv2.getTextSize('{} {}'.format(label_name, int(score)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                    cv2.rectangle(origin_img, (x1, (y1 - labelSize[1])), ((x1 + labelSize[0]), (y1 + baseLine)), (223, 128, 255), cv2.FILLED)
                    cv2.putText(origin_img, '{} {}'.format(label_name, int(score)), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
                bbox_scores.append(int(score))
            elif args.cam:
                (labelSize, baseLine) = cv2.getTextSize('{}'.format(label_name), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                cv2.rectangle(origin_img, (x1, (y1 - labelSize[1])), ((x1 + labelSize[0]), (y1 + baseLine)), (0, 102, 255), cv2.FILLED)
                cv2.putText(origin_img, '{} {}'.format(label_name, int(score)), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        if show:
            (fig, ax) = vis_bbox(img=origin_img, bbox=bboxes, label=labels, score=bbox_scores)
            fig.savefig('./docs/demo.png')
            plt.show()
        else:
            return origin_img
