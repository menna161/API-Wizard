import chainer
import chainer.functions as F
import chainer.links as L
import numpy as np
import onnx
import onnx_script
import test_case
import gen_chainercv_op_tests
import sentiment


def gen_spacetodepth_test(test_name):
    gb = onnx_script.GraphBuilder(test_name)
    small_data = np.array([0.0, 0.1, 0.2, 0.3, 1.0, 1.1, 1.2, 1.3, 2.0, 2.1, 2.2, 2.3, 3.0, 3.1, 3.2, 3.3]).reshape(1, 2, 2, 4)
    input_small = gb.input('input_small', small_data)
    output_small = np.array([0.0, 0.2, 2.0, 2.2, 0.1, 0.3, 2.1, 2.3, 1.0, 1.2, 3.0, 3.2, 1.1, 1.3, 3.1, 3.3]).reshape(1, 8, 1, 2)
    gb.output(gb.SpaceToDepth(inputs=['input_small'], blocksize=2, outputs=['output_small']), output_small)
    middle_data = np.arange(108, dtype=np.float32).reshape(2, 3, 3, 6)
    input_middle = gb.input('input_middle', middle_data)
    output_middle = np.array([0, 3, 18, 21, 36, 39, 1, 4, 19, 22, 37, 40, 2, 5, 20, 23, 38, 41, 6, 9, 24, 27, 42, 45, 7, 10, 25, 28, 43, 46, 8, 11, 26, 29, 44, 47, 12, 15, 30, 33, 48, 51, 13, 16, 31, 34, 49, 52, 14, 17, 32, 35, 50, 53, 54, 57, 72, 75, 90, 93, 55, 58, 73, 76, 91, 94, 56, 59, 74, 77, 92, 95, 60, 63, 78, 81, 96, 99, 61, 64, 79, 82, 97, 100, 62, 65, 80, 83, 98, 101, 66, 69, 84, 87, 102, 105, 67, 70, 85, 88, 103, 106, 68, 71, 86, 89, 104, 107], dtype=np.float32).reshape(2, 27, 1, 2)
    gb.output(gb.SpaceToDepth(inputs=['input_middle'], blocksize=3, outputs=['output_middle']), output_middle)
    gb.gen_test()
