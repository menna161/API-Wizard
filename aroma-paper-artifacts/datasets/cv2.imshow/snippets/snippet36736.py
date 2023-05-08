import argparse
import os
import sys
import cv2
from .. import models
from ..utils.visualization import draw_annotations, draw_boxes, draw_caption
from ..utils.anchors import anchors_for_shape, compute_gt_annotations
from ..generators import get_generators
from ..backbones import get_backbone
from ..utils.config import make_debug_config
import tf_retinanet.bin


def run(generator, config):
    ' Main loop.\n\tArgs\n\t\tgenerator : The generator used to debug.\n\t\tconfig    : Dictionary contaning debug configuration.\n\t'
    i = 0
    while True:
        image = generator.load_image(i)
        annotations = generator.load_annotations(i)
        if (len(annotations['labels']) > 0):
            if generator.transform_generator:
                (image, annotations, transform) = generator.random_transform_group_entry(image, annotations)
            if generator.visual_effect_generator:
                (image, annotations) = generator.random_visual_effect_group_entry(image, annotations)
            if config['debug']['resize']:
                (image, image_scale) = generator.resize_image(image)
                annotations['bboxes'] *= image_scale
            anchors = anchors_for_shape(image.shape)
            (positive_indices, _, max_indices) = compute_gt_annotations(anchors, annotations['bboxes'])
            if config['debug']['anchors']:
                draw_boxes(image, anchors[positive_indices], (255, 255, 0), thickness=1)
            if config['debug']['annotations']:
                draw_annotations(image, annotations, color=(0, 0, 255), label_to_name=generator.label_to_name)
                draw_boxes(image, annotations['bboxes'][(max_indices[positive_indices], :)], (0, 255, 0))
            if config['debug']['display_name']:
                draw_caption(image, [0, image.shape[0]], os.path.basename(generator.image_path(i)))
        cv2.imshow('Image', image)
        key = cv2.waitKey()
        if (key == 100):
            i = ((i + 1) % generator.size())
        if (key == 97):
            i -= 1
            if (i < 0):
                i = (generator.size() - 1)
        if ((key == ord('q')) or (key == 27)):
            return False
    return True
