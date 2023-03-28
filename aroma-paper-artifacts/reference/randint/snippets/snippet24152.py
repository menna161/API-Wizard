import cv2
import numpy as np


def random_crop(image, label, crop_size, cat_max_ratio=0.75, ignore_index=255, rng=None):
    '\n    augmentation - random cropping\n    '

    def get_crop_bbox(crop_size, img):
        'Random cropping - bounding box.'
        margin_h = max((img.shape[0] - crop_size[0]), 0)
        margin_w = max((img.shape[1] - crop_size[1]), 0)
        offset_h = rng.randint(0, (margin_h + 1))
        offset_w = rng.randint(0, (margin_w + 1))
        (crop_y1, crop_y2) = (offset_h, (offset_h + crop_size[0]))
        (crop_x1, crop_x2) = (offset_w, (offset_w + crop_size[1]))
        return (crop_y1, crop_y2, crop_x1, crop_x2)

    def crop(img, crop_bbox):
        'Crop from ``img``'
        (crop_y1, crop_y2, crop_x1, crop_x2) = crop_bbox
        return img[crop_y1:crop_y2, crop_x1:crop_x2, ...]
    crop_bbox = get_crop_bbox(crop_size, image)
    if (cat_max_ratio < 1.0):
        for _ in range(10):
            seg_temp = crop(label, crop_bbox)
            (labels, cnt) = np.unique(seg_temp, return_counts=True)
            cnt = cnt[(labels != ignore_index)]
            if ((len(cnt) > 1) and ((np.max(cnt) / np.sum(cnt)) < cat_max_ratio)):
                break
            crop_bbox = get_crop_bbox(crop_size, image)
    crop_img = crop(image, crop_bbox)
    crop_lab = crop(label, crop_bbox)
    return (crop_img, crop_lab)
