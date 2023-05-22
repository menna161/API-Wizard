import flatbuffers
from flatbuffers.compat import import_numpy


def DepthwiseConv2DOptionsAddDilationWFactor(builder, dilationWFactor):
    builder.PrependInt32Slot(5, dilationWFactor, 1)
