import flatbuffers
from flatbuffers.compat import import_numpy


def Conv2DOptionsAddStrideW(builder, strideW):
    builder.PrependInt32Slot(1, strideW, 0)
