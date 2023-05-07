import tensorflow as tf
from ..utils.anchors import AnchorParameters
from .. import initializers
from .. import layers
from . import fpn
import sys


def retinanet_bbox(model=None, nms=True, class_specific_filter=True, name='retinanet-bbox', anchor_params=None, **kwargs):
    ' Construct a RetinaNet model on top of a backbone and adds convenience functions to output boxes directly.\n\n\tThis model uses the minimum retinanet model and appends a few layers to compute boxes within the graph.\n\tThese layers include applying the regression values to the anchors and performing NMS.\n\n\tArgs\n\t\tmodel                 : RetinaNet model to append bbox layers to. If None, it will create a RetinaNet model using **kwargs.\n\t\tnms                   : Whether to use non-maximum suppression for the filtering step.\n\t\tclass_specific_filter : Whether to use class specific filtering or filter for the best scoring class only.\n\t\tname                  : Name of the model.\n\t\tanchor_params         : Struct containing anchor parameters. If None, default values are used.\n\t\t*kwargs               : Additional kwargs to pass to the minimal retinanet model.\n\n\tReturns\n\t\tA keras.models.Model which takes an image as input and outputs the detections on the image.\n\n\t\tThe order is defined as follows:\n\t\t```\n\t\t[\n\t\t\tboxes, scores, labels, other[0], other[1], ...\n\t\t]\n\t\t```\n\t'
    if (anchor_params is None):
        anchor_params = AnchorParameters.default
    if (model is None):
        model = retinanet(num_anchors=anchor_params.num_anchors(), **kwargs)
    else:
        assert_training_model(model)
    features = [model.get_layer(p_name).output for p_name in ['P3', 'P4', 'P5', 'P6', 'P7']]
    anchors = build_anchors(anchor_params, model.inputs[0], features)
    regression = model.outputs[0]
    classification = model.outputs[1]
    other = model.outputs[2:]
    boxes = layers.RegressBoxes(name='boxes')([anchors, regression])
    boxes = layers.ClipBoxes(name='clipped_boxes')([model.inputs[0], boxes])
    detections = layers.FilterDetections(nms=nms, class_specific_filter=class_specific_filter, name='filtered_detections')(([boxes, classification] + other))
    return tf.keras.models.Model(inputs=model.inputs, outputs=detections, name=name)
