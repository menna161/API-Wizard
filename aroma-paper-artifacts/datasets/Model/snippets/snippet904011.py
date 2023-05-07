import flatbuffers
from flatbuffers.compat import import_numpy
from tflite.OperatorCode import OperatorCode
from tflite.SubGraph import SubGraph
from tflite.Buffer import Buffer
from tflite.Metadata import Metadata


@classmethod
def GetRootAsModel(cls, buf, offset):
    n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
    x = Model()
    x.Init(buf, (n + offset))
    return x
