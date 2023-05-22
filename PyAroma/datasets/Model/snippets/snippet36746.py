from .common import *
import os


def get_callbacks(config, model, training_model, prediction_model, validation_generator=None, evaluation_callback=None):
    ' Returns the callbacks indicated in the config.\n\tArgs\n\t\tconfig              : Dictionary with indications about the callbacks.\n\t\tmodel               : The used model.\n\t\tprediction_model    : The used prediction model.\n\t\ttraining_model      : The used training model.\n\t\tvalidation_generator: Generator used during validation.\n\t\tevaluation_callback : Callback used to perform evaluation.\n\tReturns\n\t\tThe indicated callbacks.\n\t'
    callbacks = []
    os.makedirs(os.path.join(config['snapshots_path'], config['project_name']))
    checkpoint = tf.keras.callbacks.ModelCheckpoint(os.path.join(config['snapshots_path'], config['project_name'], '{epoch:02d}.h5'), verbose=1)
    checkpoint = RedirectModel(checkpoint, model)
    callbacks.append(checkpoint)
    if validation_generator:
        if (not evaluation_callback):
            raise NotImplementedError('Standard evaluation_callback not implement yet.')
        evaluation_callback = evaluation_callback(validation_generator)
        evaluation_callback = RedirectModel(evaluation_callback, prediction_model)
        callbacks.append(evaluation_callback)
    return callbacks
