from shapely.geometry import LineString, Polygon, MultiPolygon
import numpy as np
import cv2
import shapely
from collections import defaultdict
from skimage.transform import rescale
import glob
from skimage import io
from tqdm import tqdm
import sys


def mask_to_multipolygons(mask, epsilon=0.0, min_area=0, shift=(0, 0)):
    (contours, hierarchy) = contours_hierarchy(mask)
    if (epsilon == 0.0):
        approx_contours = contours
    else:
        approx_contours = [cv2.approxPolyDP(cnt, epsilon, True) for cnt in contours]
    if (shift != (0, 0)):
        (sx, sy) = shift
        approx_contours_shift = []
        for item in approx_contours:
            for i in item:
                i = i[0]
                approx_contours_shift.append([[(i[0] + sx), (i[1] + sy)]])
        approx_contours = [np.asarray(approx_contours_shift).astype('int32')]
    if (not contours):
        return (Polygon(), [], [])
    cnt_children = defaultdict(list)
    child_contours = set()
    assert (hierarchy.shape[0] == 1)
    for (idx, (_, _, _, parent_idx)) in enumerate(hierarchy[0]):
        if (parent_idx != (- 1)):
            child_contours.add(idx)
            cnt_children[parent_idx].append(approx_contours[idx])
    all_polygons = []
    for (idx, cnt) in enumerate(approx_contours):
        if ((idx not in child_contours) and (cv2.contourArea(cnt) >= min_area)):
            assert (cnt.shape[1] == 1)
            poly = shapely.geometry.Polygon(shell=cnt[(:, 0, :)], holes=[c[(:, 0, :)] for c in cnt_children.get(idx, []) if (cv2.contourArea(c) >= min_area)])
            all_polygons.append(poly)
    all_polygons = MultiPolygon(all_polygons)
    return (all_polygons, approx_contours, hierarchy)
