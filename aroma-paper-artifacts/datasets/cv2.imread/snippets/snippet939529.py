import numpy as np
import cv2
import os
import argparse
from tensorpack.dataflow import *


def get_data(self):
    for (fname, label) in self.imglist:
        fname = os.path.join(self.dir, fname)
        im = cv2.imread(fname)
        assert (im is not None), fname
        with open(fname, 'rb') as f:
            jpeg = f.read()
        jpeg = np.asarray(bytearray(jpeg), dtype='uint8')
        assert (len(jpeg) > 10)
        (yield [jpeg, label])
