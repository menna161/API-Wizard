from model import net
from argparse import ArgumentParser
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import tensorflow as tf
import numpy as np
from tqdm import tqdm
from helper import showClassTable, maybeExtract, maybeDownloadOrExtract, GroundTruthVisualise


def Patch(height_index, width_index):
    transpose_array = input_mat
    height_slice = slice(height_index, (height_index + PATCH_SIZE))
    width_slice = slice(width_index, (width_index + PATCH_SIZE))
    patch = transpose_array[(height_slice, width_slice, :)]
    mean_normalized_patch = []
    for i in range(BAND):
        mean_normalized_patch.append((patch[(:, :, i)] - MEAN_ARRAY[i]))
    mean_normalized_patch = np.array(mean_normalized_patch).astype(np.float16)
    mean_normalized_patch = np.transpose(mean_normalized_patch, (1, 2, 0))
    return mean_normalized_patch
