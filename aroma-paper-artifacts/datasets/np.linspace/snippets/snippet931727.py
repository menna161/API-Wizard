import numpy as np


def eval_plane_and_pixel_recall_normal(segmentation, gt_segmentation, param, gt_param, threshold=0.5):
    '\n    :param segmentation: label map for plane segmentation [h, w] where 20 indicate non-planar\n    :param gt_segmentation: ground truth label for plane segmentation where 20 indicate non-planar\n    :param threshold: value for iou\n    :return: percentage of correctly predicted ground truth planes correct plane\n    '
    depth_threshold_list = np.linspace(0.0, 30, 13)
    plane_num = (len(np.unique(segmentation)) - 1)
    gt_plane_num = (len(np.unique(gt_segmentation)) - 1)
    plane_recall = np.zeros((gt_plane_num, len(depth_threshold_list)))
    pixel_recall = np.zeros((gt_plane_num, len(depth_threshold_list)))
    plane_area = 0.0
    gt_param = gt_param.reshape(20, 3)
    for i in range(gt_plane_num):
        gt_plane = (gt_segmentation == i)
        plane_area += np.sum(gt_plane)
        for j in range(plane_num):
            pred_plane = (segmentation == j)
            iou = eval_iou(gt_plane, pred_plane)
            if (iou > threshold):
                gt_p = gt_param[i]
                pred_p = param[j]
                n_gt_p = (gt_p / np.linalg.norm(gt_p))
                n_pred_p = (pred_p / np.linalg.norm(pred_p))
                angle = np.arccos(np.clip(np.dot(n_gt_p, n_pred_p), (- 1.0), 1.0))
                degree = np.degrees(angle)
                depth_diff = degree
                plane_recall[i] = (depth_diff < depth_threshold_list).astype(np.float32)
                pixel_recall[i] = ((depth_diff < depth_threshold_list).astype(np.float32) * np.sum((gt_plane * pred_plane)))
                break
    pixel_recall = (np.sum(pixel_recall, axis=0).reshape(1, (- 1)) / plane_area)
    return (plane_recall, pixel_recall)
