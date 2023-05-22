import os
import numpy as np
import keras.backend as K
from keras.layers import Input, Lambda
from keras.models import Model
from keras.optimizers import Adam
from keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from yolo3.model import preprocess_true_boxes, yolo_body, tiny_yolo_body, yolo_loss
from yolo3.utils import get_random_data


def create_model(input_shape, anchors, num_classes, load_pretrained=True, freeze_body=2, weights_path='model_data/yolo_weights.h5'):
    'create the training model'
    K.clear_session()
    image_input = Input(shape=(None, None, 3))
    (h, w) = input_shape
    num_anchors = len(anchors)
    y_true = [Input(shape=((h // {0: 32, 1: 16, 2: 8}[l]), (w // {0: 32, 1: 16, 2: 8}[l]), (num_anchors // 3), (num_classes + 5))) for l in range(3)]
    model_body = yolo_body(image_input, (num_anchors // 3), num_classes)
    print('Create YOLOv3 model with {} anchors and {} classes.'.format(num_anchors, num_classes))
    if load_pretrained:
        model_body.load_weights(weights_path, by_name=True, skip_mismatch=True)
        print('Load weights {}.'.format(weights_path))
        if (freeze_body in [1, 2]):
            num = (185, (len(model_body.layers) - 3))[(freeze_body - 1)]
            for i in range(num):
                model_body.layers[i].trainable = False
            print('Freeze the first {} layers of total {} layers.'.format(num, len(model_body.layers)))
    out1 = model_body.layers[246].output
    out2 = model_body.layers[247].output
    out3 = model_body.layers[248].output
    bottleneck_model = Model([model_body.input, *y_true], [out1, out2, out3])
    in0 = Input(shape=bottleneck_model.output[0].shape[1:].as_list())
    in1 = Input(shape=bottleneck_model.output[1].shape[1:].as_list())
    in2 = Input(shape=bottleneck_model.output[2].shape[1:].as_list())
    last_out0 = model_body.layers[249](in0)
    last_out1 = model_body.layers[250](in1)
    last_out2 = model_body.layers[251](in2)
    model_last = Model(inputs=[in0, in1, in2], outputs=[last_out0, last_out1, last_out2])
    model_loss_last = Lambda(yolo_loss, output_shape=(1,), name='yolo_loss', arguments={'anchors': anchors, 'num_classes': num_classes, 'ignore_thresh': 0.5})([*model_last.output, *y_true])
    last_layer_model = Model([in0, in1, in2, *y_true], model_loss_last)
    model_loss = Lambda(yolo_loss, output_shape=(1,), name='yolo_loss', arguments={'anchors': anchors, 'num_classes': num_classes, 'ignore_thresh': 0.5})([*model_body.output, *y_true])
    model = Model([model_body.input, *y_true], model_loss)
    return (model, bottleneck_model, last_layer_model)
