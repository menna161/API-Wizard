import numpy as np
import keras.backend as K
from keras.layers import Input, Lambda
from keras.models import Model
from keras.optimizers import Adam
from keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from yolo3.model import preprocess_true_boxes, yolo_body, tiny_yolo_body, yolo_loss
from yolo3.utils import get_random_data


def create_tiny_model(input_shape, anchors, num_classes, load_pretrained=True, freeze_body=2, weights_path='model_data/tiny_yolo_weights.h5'):
    'create the training model, for Tiny YOLOv3'
    K.clear_session()
    image_input = Input(shape=(None, None, 3))
    (h, w) = input_shape
    num_anchors = len(anchors)
    y_true = [Input(shape=((h // {0: 32, 1: 16}[l]), (w // {0: 32, 1: 16}[l]), (num_anchors // 2), (num_classes + 5))) for l in range(2)]
    model_body = tiny_yolo_body(image_input, (num_anchors // 2), num_classes)
    print('Create Tiny YOLOv3 model with {} anchors and {} classes.'.format(num_anchors, num_classes))
    if load_pretrained:
        model_body.load_weights(weights_path, by_name=True, skip_mismatch=True)
        print('Load weights {}.'.format(weights_path))
        if (freeze_body in [1, 2]):
            num = (20, (len(model_body.layers) - 2))[(freeze_body - 1)]
            for i in range(num):
                model_body.layers[i].trainable = False
            print('Freeze the first {} layers of total {} layers.'.format(num, len(model_body.layers)))
    model_loss = Lambda(yolo_loss, output_shape=(1,), name='yolo_loss', arguments={'anchors': anchors, 'num_classes': num_classes, 'ignore_thresh': 0.7})([*model_body.output, *y_true])
    model = Model([model_body.input, *y_true], model_loss)
    return model
