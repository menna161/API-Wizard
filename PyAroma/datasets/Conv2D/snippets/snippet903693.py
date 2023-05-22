import flatbuffers
from flatbuffers.compat import import_numpy


def Conv2DOptionsAddDilationWFactor(builder, dilationWFactor):
    builder.PrependInt32Slot(4, dilationWFactor, 1)
