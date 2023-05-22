import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization, cnn_regularization
from ccn.cfg import get_config


def Perceptor():
    'Use a pretrained model to use in calculating a perceptual loss score\n  '
    (ModelFunc, PerceptorLayerName) = get_pretrained_info()
    Perceptor = ModelFunc(include_top=False, weights='imagenet', input_shape=(CFG['y_dim'], CFG['x_dim'], 3))
    PerceptorLayer = Perceptor.get_layer(PerceptorLayerName)
    Perceptor = tf.keras.Model(inputs=Perceptor.inputs, outputs=[PerceptorLayer.output])
    print(f'Perceptor output: {Perceptor.layers[(- 1)].output}')
    return Perceptor
