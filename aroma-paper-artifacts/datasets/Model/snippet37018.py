import shutil
import chainer
import numpy as np
import onnx_chainer
from test_case import TestCase


def create_backprop_test(test_name, fn, args, dtype=np.float32, **kwargs):
    test_dir = ('out/%s' % test_name)
    params = {}
    for (name, value) in kwargs.items():
        params[name] = np.array(value, dtype)
    model = AnyModel(fn, params)
    chainer.disable_experimental_feature_warning = True
    shutil.rmtree(test_dir, ignore_errors=True)
    onnx_chainer.export_testcase(model, args, test_dir, output_grad=True, output_names='loss')
