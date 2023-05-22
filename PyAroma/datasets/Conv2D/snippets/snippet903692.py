import flatbuffers
from flatbuffers.compat import import_numpy


def Conv2DOptionsAddFusedActivationFunction(builder, fusedActivationFunction):
    builder.PrependInt8Slot(3, fusedActivationFunction, 0)
