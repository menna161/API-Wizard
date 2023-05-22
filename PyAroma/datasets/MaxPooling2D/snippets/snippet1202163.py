import tensorflow as tf
import keras.backend as K
import keras.layers as KL
import keras.models as KM
import os
import numpy as np
import keras.optimizers
from keras.datasets import mnist
from keras.preprocessing.image import ImageDataGenerator

if (__name__ == '__main__'):
    import os
    import numpy as np
    import keras.optimizers
    from keras.datasets import mnist
    from keras.preprocessing.image import ImageDataGenerator
    GPU_COUNT = 2
    ROOT_DIR = os.path.abspath('../')
    MODEL_DIR = os.path.join(ROOT_DIR, 'logs')

    def build_model(x_train, num_classes):
        tf.reset_default_graph()
        inputs = KL.Input(shape=x_train.shape[1:], name='input_image')
        x = KL.Conv2D(32, (3, 3), activation='relu', padding='same', name='conv1')(inputs)
        x = KL.Conv2D(64, (3, 3), activation='relu', padding='same', name='conv2')(x)
        x = KL.MaxPooling2D(pool_size=(2, 2), name='pool1')(x)
        x = KL.Flatten(name='flat1')(x)
        x = KL.Dense(128, activation='relu', name='dense1')(x)
        x = KL.Dense(num_classes, activation='softmax', name='dense2')(x)
        return KM.Model(inputs, x, 'digit_classifier_model')
    ((x_train, y_train), (x_test, y_test)) = mnist.load_data()
    x_train = (np.expand_dims(x_train, (- 1)).astype('float32') / 255)
    x_test = (np.expand_dims(x_test, (- 1)).astype('float32') / 255)
    print('x_train shape:', x_train.shape)
    print('x_test shape:', x_test.shape)
    datagen = ImageDataGenerator()
    model = build_model(x_train, 10)
    model = ParallelModel(model, GPU_COUNT)
    optimizer = keras.optimizers.SGD(lr=0.01, momentum=0.9, clipnorm=5.0)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    model.summary()
    model.fit_generator(datagen.flow(x_train, y_train, batch_size=64), steps_per_epoch=50, epochs=10, verbose=1, validation_data=(x_test, y_test), callbacks=[keras.callbacks.TensorBoard(log_dir=MODEL_DIR, write_graph=True)])
