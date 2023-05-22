import flatbuffers
from flatbuffers.compat import import_numpy


def DepthwiseConv2DOptionsAddFusedActivationFunction(builder, fusedActivationFunction):
    builder.PrependInt8Slot(4, fusedActivationFunction, 0)
