import argparse
import cv2
from tensorpack import *
from tensorpack.dataflow.imgaug import *
from tensorpack.dataflow.parallel import PlasmaGetData, PlasmaPutData
from tensorpack.utils.serialize import loads
import augmentors


def test_inference(dir, name, augs, batch=128):
    ds = dataset.ILSVRC12Files(dir, name, shuffle=False, dir_structure='train')
    aug = imgaug.AugmentorList(augs)

    def mapf(dp):
        (fname, cls) = dp
        im = cv2.imread(fname, cv2.IMREAD_COLOR)
        im = aug.augment(im)
        return (im, cls)
    ds = MultiThreadMapData(ds, 30, mapf, buffer_size=2000, strict=True)
    ds = BatchData(ds, batch)
    ds = MultiProcessRunnerZMQ(ds, 1)
    return ds
