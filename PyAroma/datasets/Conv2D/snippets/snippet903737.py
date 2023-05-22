import flatbuffers
from flatbuffers.compat import import_numpy


def DepthwiseConv2DOptionsAddDepthMultiplier(builder, depthMultiplier):
    builder.PrependInt32Slot(3, depthMultiplier, 0)
