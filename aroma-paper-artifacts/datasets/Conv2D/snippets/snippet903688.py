import flatbuffers
from flatbuffers.compat import import_numpy


def Conv2DOptionsStart(builder):
    builder.StartObject(6)
