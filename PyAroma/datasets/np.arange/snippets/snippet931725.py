import numpy as np


def eval_plane_prediction(predSegmentations, gtSegmentations, predDepths, gtDepths, threshold=0.5):
    predNumPlanes = (len(np.unique(predSegmentations)) - 1)
    gtNumPlanes = (len(np.unique(gtSegmentations)) - 1)
    if (len(gtSegmentations.shape) == 2):
        gtSegmentations = (np.expand_dims(gtSegmentations, (- 1)) == np.arange(gtNumPlanes)).astype(np.float32)
    if (len(predSegmentations.shape) == 2):
        predSegmentations = (np.expand_dims(predSegmentations, (- 1)) == np.arange(predNumPlanes)).astype(np.float32)
    planeAreas = gtSegmentations.sum(axis=(0, 1))
    intersectionMask = ((np.expand_dims(gtSegmentations, (- 1)) * np.expand_dims(predSegmentations, 2)) > 0.5)
    depthDiffs = (gtDepths - predDepths)
    depthDiffs = depthDiffs[(:, :, np.newaxis, np.newaxis)]
    intersection = np.sum(intersectionMask.astype(np.float32), axis=(0, 1))
    planeDiffs = (np.abs((depthDiffs * intersectionMask)).sum(axis=(0, 1)) / np.maximum(intersection, 0.0001))
    planeDiffs[(intersection < 0.0001)] = 1
    union = np.sum(((np.expand_dims(gtSegmentations, (- 1)) + np.expand_dims(predSegmentations, 2)) > 0.5).astype(np.float32), axis=(0, 1))
    planeIOUs = (intersection / np.maximum(union, 0.0001))
    numPredictions = int(predSegmentations.max(axis=(0, 1)).sum())
    numPixels = planeAreas.sum()
    IOUMask = (planeIOUs > threshold).astype(np.float32)
    minDiff = np.min(((planeDiffs * IOUMask) + (1000000 * (1 - IOUMask))), axis=1)
    stride = 0.05
    pixelRecalls = []
    planeStatistics = []
    for step in range(int(((0.61 / stride) + 1))):
        diff = (step * stride)
        pixelRecalls.append((np.minimum(((intersection * (planeDiffs <= diff).astype(np.float32)) * IOUMask).sum(1), planeAreas).sum() / numPixels))
        planeStatistics.append(((minDiff <= diff).sum(), gtNumPlanes, numPredictions))
    return (pixelRecalls, planeStatistics)
