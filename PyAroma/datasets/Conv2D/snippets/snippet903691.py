import flatbuffers
from flatbuffers.compat import import_numpy


def Conv2DOptionsAddStrideH(builder, strideH):
    builder.PrependInt32Slot(2, strideH, 0)