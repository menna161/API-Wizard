from .anchors import compute_overlap
from .visualization import draw_detections, draw_annotations
import tensorflow as tf
import numpy as np
import os
import time
import cv2
import progressbar


def evaluate(generator, model, iou_threshold=0.5, score_threshold=0.05, max_detections=100, save_path=None):
    ' Evaluate a given dataset using a given model.\n\t# Arguments\n\t\tgenerator       : The generator that represents the dataset to evaluate.\n\t\tmodel           : The model to evaluate.\n\t\tiou_threshold   : The threshold used to consider when a detection is positive or negative.\n\t\tscore_threshold : The score confidence threshold to use for detections.\n\t\tmax_detections  : The maximum number of detections to use per image.\n\t\tsave_path       : The path to save images with visualized detections to.\n\t# Returns\n\t\tA dict mapping class names to mAP scores.\n\t'
    (all_detections, all_inferences) = _get_detections(generator, model, score_threshold=score_threshold, max_detections=max_detections, save_path=save_path)
    all_annotations = _get_annotations(generator)
    average_precisions = {}
    for label in range(generator.num_classes()):
        if (not generator.has_label(label)):
            continue
        false_positives = np.zeros((0,))
        true_positives = np.zeros((0,))
        scores = np.zeros((0,))
        num_annotations = 0.0
        for i in range(generator.size()):
            detections = all_detections[i][label]
            annotations = all_annotations[i][label]
            num_annotations += annotations.shape[0]
            detected_annotations = []
            for d in detections:
                scores = np.append(scores, d[4])
                if (annotations.shape[0] == 0):
                    false_positives = np.append(false_positives, 1)
                    true_positives = np.append(true_positives, 0)
                    continue
                overlaps = compute_overlap(np.expand_dims(d, axis=0), annotations)
                assigned_annotation = np.argmax(overlaps, axis=1)
                max_overlap = overlaps[(0, assigned_annotation)]
                if ((max_overlap >= iou_threshold) and (assigned_annotation not in detected_annotations)):
                    false_positives = np.append(false_positives, 0)
                    true_positives = np.append(true_positives, 1)
                    detected_annotations.append(assigned_annotation)
                else:
                    false_positives = np.append(false_positives, 1)
                    true_positives = np.append(true_positives, 0)
        if (num_annotations == 0):
            average_precisions[label] = (0, 0)
            continue
        indices = np.argsort((- scores))
        false_positives = false_positives[indices]
        true_positives = true_positives[indices]
        false_positives = np.cumsum(false_positives)
        true_positives = np.cumsum(true_positives)
        recall = (true_positives / num_annotations)
        precision = (true_positives / np.maximum((true_positives + false_positives), np.finfo(np.float64).eps))
        average_precision = _compute_ap(recall, precision)
        average_precisions[label] = (average_precision, num_annotations)
        inference_time = (np.sum(all_inferences) / generator.size())
    print_results(generator, average_precisions, inference_time)
