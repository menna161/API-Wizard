import flatbuffers
from flatbuffers.compat import import_numpy


def DepthwiseConv2DOptionsAddDilationHFactor(builder, dilationHFactor):
    builder.PrependInt32Slot(6, dilationHFactor, 1)
