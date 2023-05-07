import cv2
import random
import numpy as np
import torch
from torch.utils.data import Dataset


def load_image_and_bboxes_with_cutmix(self, index):
    (image, bboxes) = self.load_image_and_boxes(index)
    (image_to_be_mixed, bboxes_to_be_mixed) = self.load_image_and_boxes(random.randint(0, (self.image_ids.shape[0] - 1)))
    image_size = image.shape[0]
    (cutoff_x1, cutoff_y1) = [int(random.uniform((image_size * 0.0), (image_size * 0.49))) for _ in range(2)]
    (cutoff_x2, cutoff_y2) = [int(random.uniform((image_size * 0.5), (image_size * 1.0))) for _ in range(2)]
    image_cutmix = image.copy()
    image_cutmix[(cutoff_y1:cutoff_y2, cutoff_x1:cutoff_x2)] = image_to_be_mixed[(cutoff_y1:cutoff_y2, cutoff_x1:cutoff_x2)]
    bboxes_not_intersect = bboxes[np.concatenate((np.where((bboxes[(:, 0)] > cutoff_x2)), np.where((bboxes[(:, 2)] < cutoff_x1)), np.where((bboxes[(:, 1)] > cutoff_y2)), np.where((bboxes[(:, 3)] < cutoff_y1))), axis=None)]
    bboxes_intersect = bboxes.copy()
    top_intersect = np.where(((((bboxes[(:, 0)] < cutoff_x2) & (bboxes[(:, 2)] > cutoff_x1)) & (bboxes[(:, 1)] < cutoff_y2)) & (bboxes[(:, 3)] > cutoff_y2)))
    right_intersect = np.where(((((bboxes[(:, 0)] < cutoff_x2) & (bboxes[(:, 2)] > cutoff_x2)) & (bboxes[(:, 1)] < cutoff_y2)) & (bboxes[(:, 3)] > cutoff_y1)))
    bottom_intersect = np.where(((((bboxes[(:, 0)] < cutoff_x2) & (bboxes[(:, 2)] > cutoff_x1)) & (bboxes[(:, 1)] < cutoff_y1)) & (bboxes[(:, 3)] > cutoff_y1)))
    left_intersect = np.where(((((bboxes[(:, 0)] < cutoff_x1) & (bboxes[(:, 2)] > cutoff_x1)) & (bboxes[(:, 1)] < cutoff_y2)) & (bboxes[(:, 3)] > cutoff_y1)))
    right_intersect = np.setdiff1d(right_intersect, top_intersect)
    right_intersect = np.setdiff1d(right_intersect, bottom_intersect)
    right_intersect = np.setdiff1d(right_intersect, left_intersect)
    bottom_intersect = np.setdiff1d(bottom_intersect, top_intersect)
    bottom_intersect = np.setdiff1d(bottom_intersect, left_intersect)
    left_intersect = np.setdiff1d(left_intersect, top_intersect)
    bboxes_intersect[(:, 1)][top_intersect] = cutoff_y2
    bboxes_intersect[(:, 0)][right_intersect] = cutoff_x2
    bboxes_intersect[(:, 3)][bottom_intersect] = cutoff_y1
    bboxes_intersect[(:, 2)][left_intersect] = cutoff_x1
    bboxes_intersect[(:, 1)][top_intersect] = cutoff_y2
    bboxes_intersect[(:, 0)][right_intersect] = cutoff_x2
    bboxes_intersect[(:, 3)][bottom_intersect] = cutoff_y1
    bboxes_intersect[(:, 2)][left_intersect] = cutoff_x1
    bboxes_intersect = bboxes_intersect[np.concatenate((top_intersect, right_intersect, bottom_intersect, left_intersect), axis=None)]
    bboxes_to_be_mixed[(:, [0, 2])] = bboxes_to_be_mixed[(:, [0, 2])].clip(min=cutoff_x1, max=cutoff_x2)
    bboxes_to_be_mixed[(:, [1, 3])] = bboxes_to_be_mixed[(:, [1, 3])].clip(min=cutoff_y1, max=cutoff_y2)
    bboxes_cutmix = np.vstack((bboxes_not_intersect, bboxes_intersect, bboxes_to_be_mixed)).astype(int)
    bboxes_cutmix = bboxes_cutmix[np.where((((bboxes_cutmix[(:, 2)] - bboxes_cutmix[(:, 0)]) * (bboxes_cutmix[(:, 3)] - bboxes_cutmix[(:, 1)])) > 500))]
    return (image_cutmix, bboxes_cutmix)
