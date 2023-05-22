import tensorflow as tf
import cv2
import os
from configuration import OBJECT_CLASSES, save_model_dir, test_picture_dir, NUM_CLASSES
from core.inference import InferenceProcedure
from core.ssd import SSD
from utils.tools import preprocess_image, resize_box


def test_single_picture(picture_dir, model):
    image_tensor = preprocess_image(picture_dir)
    image_tensor = tf.expand_dims(image_tensor, axis=0)
    image_array = cv2.imread(picture_dir)
    (h, w, _) = image_array.shape
    procedure = InferenceProcedure(model=model, num_classes=NUM_CLASSES)
    results = procedure(image_tensor)
    results = tf.squeeze(results, axis=0)
    filter_mask = (results[(:, :, 0)] > 0.6)
    filter_mask = tf.expand_dims(filter_mask, axis=(- 1))
    filter_mask = tf.broadcast_to(filter_mask, shape=results.shape)
    results = tf.boolean_mask(results, filter_mask)
    results = tf.reshape(results, shape=((- 1), 6))
    scores = results[(:, 0)].numpy()
    boxes = results[(:, 1:5)].numpy()
    boxes = resize_box(boxes, h, w)
    classes = tf.cast(results[(:, (- 1))], dtype=tf.int32).numpy()
    image_with_boxes = draw_boxes_on_image(image_array, boxes, scores, classes)
    return image_with_boxes
