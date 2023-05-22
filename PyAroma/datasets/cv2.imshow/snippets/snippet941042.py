import tensorflow as tf
import cv2
import os
from configuration import OBJECT_CLASSES, save_model_dir, test_picture_dir, NUM_CLASSES
from core.inference import InferenceProcedure
from core.ssd import SSD
from utils.tools import preprocess_image, resize_box

if (__name__ == '__main__'):
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.list_logical_devices('GPU')
            print(len(gpus), 'Physical GPUs,', len(logical_gpus), 'Logical GPUs')
        except RuntimeError as e:
            print(e)
    ssd_model = SSD()
    last_epoch = os.listdir(save_model_dir)[(- 2)].split('.')[0]
    ssd_model.load_weights(filepath=(save_model_dir + last_epoch))
    image = test_single_picture(picture_dir=test_picture_dir, model=ssd_model)
    cv2.namedWindow('detect result', flags=cv2.WINDOW_NORMAL)
    cv2.imshow('detect result', image)
    cv2.waitKey(0)
