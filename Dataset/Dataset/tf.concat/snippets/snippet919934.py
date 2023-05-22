import tensorflow as tf
import numpy as np


def net(statlieImg, prob, HEIGHT, WIDTH, CHANNELS, N_PARALLEL_BAND, NUM_CLASS):
    sequence = {}
    sequence['input'] = tf.reshape(statlieImg, [(- 1), HEIGHT, WIDTH, CHANNELS])
    with tf.variable_scope('conv1'):
        layer = sequence['input']
        layer = create_conv_2dlayer(input=layer, filter_size=1, num_output_channel=CHANNELS, relu=True, padding='valid')
        sequence['conv1'] = layer
    with tf.variable_scope('parallelProcess'):
        layer = sequence['conv1']
        with tf.variable_scope('reshape3d'):
            layer = tf.reshape(layer, [(- 1), HEIGHT, WIDTH, CHANNELS, 1])
        with tf.variable_scope('split'):
            layer = tf.split(layer, num_or_size_splits=N_PARALLEL_BAND, axis=3)
        with tf.variable_scope('segmentation', reuse=tf.AUTO_REUSE):
            for (index, l) in enumerate(layer):
                with tf.variable_scope('layer1'):
                    layer1 = create_conv_3dlayer(input=l, filter_width=2, filter_height=2, filter_depth=9, stride=2, num_output_channels=1, relu=True)
                with tf.variable_scope('layer2'):
                    layer2 = create_conv_3dlayer(input=layer1, filter_width=3, filter_height=3, filter_depth=5, stride=1, num_output_channels=3, relu=True)
                with tf.variable_scope('layer3'):
                    layer3 = create_conv_3dlayer(input=layer2, filter_width=2, filter_height=2, filter_depth=3, stride=2, num_output_channels=6, relu=True)
                with tf.variable_scope('layer4'):
                    layer4 = create_conv_3dlayer(input=layer3, filter_width=1, filter_height=1, filter_depth=3, stride=1, num_output_channels=10, relu=True)
                (layer5, _) = flatten_layer(layer4)
                if (not index):
                    stack = tf.concat([layer5], axis=1)
                else:
                    stack = tf.concat([stack, layer5], axis=1)
        sequence['parallel_end'] = stack
    with tf.variable_scope('dense1'):
        layer = sequence['parallel_end']
        (layer, number_features) = flatten_layer(layer)
        layer = fully_connected_layer(input=layer, num_inputs=number_features, num_outputs=120, activation='relu')
        layer = tf.nn.dropout(x=layer, keep_prob=prob)
        sequence['dense1'] = layer
    with tf.variable_scope('dense3'):
        layer = sequence['dense1']
        layer = fully_connected_layer(input=layer, num_inputs=120, num_outputs=NUM_CLASS)
        sequence['dense3'] = layer
    y_predict = tf.nn.softmax(sequence['dense3'])
    sequence['class_prediction'] = y_predict
    sequence['predict_class_number'] = tf.argmax(y_predict, axis=1)
    return sequence
