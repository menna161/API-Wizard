import flatbuffers
from flatbuffers.compat import import_numpy


def DepthwiseConv2DOptionsStart(builder):
    builder.StartObject(7)
