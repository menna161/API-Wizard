from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import mxnet as mx
from gluoncv import model_zoo
from gluoncv2.model_provider import get_model as gcv2_get_model, _models as gcv2_models
from pprint import pprint


def __init__(self, embed_dim, ctx):
    super(Model, self).__init__()
    self.embed_dim = embed_dim
    self.ctx = ctx
    self.backbone = Backbone('googlenet', ctx)
    with self.name_scope():
        self.embedding_layer = mx.gluon.nn.Dense(embed_dim, weight_initializer=mx.initializer.Xavier(magnitude=2))
        self.pooling_layer = mx.gluon.nn.GlobalAvgPool2D()
    self.embedding_layer.initialize(ctx=ctx)
    self.pooling_layer.initialize(ctx=ctx)
