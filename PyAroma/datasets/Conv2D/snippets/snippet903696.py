import flatbuffers
from flatbuffers.compat import import_numpy


@classmethod
def GetRootAsConv2DOptions(cls, buf, offset):
    n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
    x = Conv2DOptions()
    x.Init(buf, (n + offset))
    return x
