from model import net
from argparse import ArgumentParser
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import tensorflow as tf
import numpy as np
from tqdm import tqdm
from helper import showClassTable, maybeExtract, maybeDownloadOrExtract, GroundTruthVisualise


def pixelClassification():
    (input_mat, _) = maybeDownloadOrExtract(opt.data)
    (input_height, input_width) = (input_mat.shape[0], input_mat.shape[1])
    BAND = input_mat.shape[2]
    PATCH_SIZE = opt.patch_size
    MEAN_ARRAY = np.ndarray(shape=(BAND, 1))
    new_input_mat = []
    calib_val_pad = int(((PATCH_SIZE - 1) / 2))
    for i in range(BAND):
        MEAN_ARRAY[i] = np.mean(input_mat[(:, :, i)])
        new_input_mat.append(np.pad(input_mat[(:, :, i)], calib_val_pad, 'constant', constant_values=0))
    new_input_mat = np.transpose(new_input_mat, (1, 2, 0))
    input_mat = new_input_mat

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
    labelled_img = np.ndarray(shape=(input_height, input_width))
    for i in tqdm(range((input_height - 1))):
        for j in range((input_width - 1)):
            current_input = Patch(i, j)
            current_input = np.expand_dims(current_input, axis=0)
            feed_dict_test = {img_entry: current_input, prob: 1.0}
            prediction = session.run(model['predict_class_number'], feed_dict=feed_dict_test)
            labelled_img[(i, j)] = prediction[0]
    labelled_img += 1
    labelled_img = np.pad(labelled_img, [(0, 1), (0, 0)], 'constant', constant_values=(0, 0))
    print(np.min(labelled_img), np.max(labelled_img), labelled_img.shape)
    GroundTruthVisualise(labelled_img, opt.data, False)
