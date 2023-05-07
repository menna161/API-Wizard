import tensorflow as tf
from ..utils.anchors import AnchorParameters
from .. import initializers
from .. import layers
from . import fpn
import sys


def retinanet(inputs, backbone_layers, submodels, num_anchors=None, create_pyramid_features=fpn.create_pyramid_features, name='retinanet'):
    ' Construct a RetinaNet model on top of a backbone.\n\tThis model is the minimum model necessary for training (with the unfortunate exception of anchors as output).\n\tArgs\n\t\tinputs                  : keras.layers.Input (or list of) for the input to the model.\n\t\tnum_anchors             : Number of base anchors.\n\t\tcreate_pyramid_features : Functor for creating pyramid features given the features C3, C4, C5 from the backbone.\n\t\tsubmodels               : Submodels to run on each feature map (default is regression and classification submodels).\n\t\tname                    : Name of the model.\n\tReturns\n\t\tA keras.models.Model which takes an image as input and outputs generated anchors and the result from each submodel on every pyramid level.\n\t\tThe order of the outputs is as defined in submodels:\n\t\t```\n\t\t[\n\t\t\tregression, classification, other[0], other[1], ...\n\t\t]\n\t\t```\n\t'
    if (num_anchors is None):
        num_anchors = AnchorParameters.default.num_anchors()
    retinanet_submodels = []
    for submodel in submodels:
        retinanet_submodels.append((submodel.get_name(), submodel.create(num_anchors=num_anchors, name='{}_submodel'.format(submodel.get_name()))))
    (C3, C4, C5) = backbone_layers
    features = create_pyramid_features(C3, C4, C5)
    pyramids = fpn.build_pyramid(retinanet_submodels, features)
    return tf.keras.models.Model(inputs=inputs, outputs=pyramids, name=name)
