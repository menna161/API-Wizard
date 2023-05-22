import flatbuffers
from flatbuffers.compat import import_numpy


@classmethod
def GetRootAsDepthwiseConv2DOptions(cls, buf, offset):
    n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
    x = DepthwiseConv2DOptions()
    x.Init(buf, (n + offset))
    return x
