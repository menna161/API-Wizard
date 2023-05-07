from __future__ import print_function
import numpy as np
import json
import os
import torch


def evaluate(generator, retinanet, iou_threshold=0.5, score_threshold=0.05, max_detections=100, save_path=None):
    ' Evaluate a given dataset using a given retinanet.\n    # Arguments\n        generator       : The generator that represents the dataset to evaluate.\n        retinanet           : The retinanet to evaluate.\n        iou_threshold   : The threshold used to consider when a detection is positive or negative.\n        score_threshold : The score confidence threshold to use for detections.\n        max_detections  : The maximum number of detections to use per image.\n        save_path       : The path to save images with visualized detections to.\n    # Returns\n        A dict mapping class names to mAP scores.\n    '
    all_detections = _get_detections(generator, retinanet, score_threshold=score_threshold, max_detections=max_detections, save_path=save_path)
    all_annotations = _get_annotations(generator)
    average_precisions = {}
    for label in range(generator.num_classes()):
        false_positives = np.zeros((0,))
        true_positives = np.zeros((0,))
        scores = np.zeros((0,))
        num_annotations = 0.0
        for i in range(len(generator)):
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
    print('\nmAP:')
    for label in range(generator.num_classes()):
        label_name = generator.label_to_name(label)
        print('{}: {}'.format(label_name, average_precisions[label][0]))
    return average_precisions
