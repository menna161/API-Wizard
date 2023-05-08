import flatbuffers
from flatbuffers.compat import import_numpy


def Conv2DOptionsAddDilationHFactor(builder, dilationHFactor):
    builder.PrependInt32Slot(5, dilationHFactor, 1)
