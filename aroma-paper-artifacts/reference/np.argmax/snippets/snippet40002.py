import numpy as np
from segmentation_models import UnetRegressor, Unet
from dataFunctions import *
from keras.callbacks import ModelCheckpoint
from keras.layers import Input
from keras.models import load_model
from keras import backend as K
from tqdm import tqdm
import json
import tensorflow as tf


def test(self):
    '\n        Launches testing, which saves output files\n        :return: None\n        '
    input_tensor = Input(shape=(self.params.IMG_SZ[0], self.params.IMG_SZ[1], self.params.NUM_CHANNELS))
    input_shape = (self.params.IMG_SZ[0], self.params.IMG_SZ[1], self.params.NUM_CHANNELS)
    model = self.get_model(None, input_tensor, input_shape)
    if (self.mode == self.params.SEMANTIC_MODE):
        numPredChannels = self.params.NUM_CATEGORIES
        outReplaceStr = self.params.CLSPRED_FILE_STR
        model = self.build_model()
        model.load_weights(self.params.SEMANTIC_TEST_MODEL, by_name=True)
    elif (self.mode == self.params.SINGLEVIEW_MODE):
        numPredChannels = 1
        outReplaceStr = self.params.AGLPRED_FILE_STR
        model = self.build_model()
        model.load_weights(self.params.SINGLEVIEW_TEST_MODEL, by_name=True)
    model.summary()
    imgPaths = get_image_paths(self.params, isTest=True)
    print('Number of files = ', len(imgPaths))
    for imgPath in tqdm(imgPaths):
        imageName = os.path.split(imgPath)[(- 1)]
        outName = imageName.replace(self.params.IMG_FILE_STR, outReplaceStr)
        img = np.expand_dims(load_img(imgPath), axis=0).astype('float32')
        img = image_batch_preprocess(img, self.params, self.meanVals)
        pred = model.predict(img)[(0, :, :, :)]
        if (self.mode == self.params.SEMANTIC_MODE):
            if (self.params.NUM_CATEGORIES > 1):
                pred = np.argmax(pred, axis=2).astype('uint8')
            else:
                pred = (pred > self.params.BINARY_CONF_TH).astype('uint8')
            if self.params.CONVERT_LABELS:
                pred = convert_labels(pred, self.params, toLasStandard=True)
        else:
            pred = pred[(:, :, 0)]
        tifffile.imsave(os.path.join(self.params.OUTPUT_DIR, outName), pred, compress=6)
