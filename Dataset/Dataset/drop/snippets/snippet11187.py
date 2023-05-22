import unittest
from nmigen import *
from nmigen.back.pysim import *
from ._util import *
from ..usb.mux import *
from ..usb.endpoint import *


def test_w_drop(self):
    dut = DoubleBuffer(depth=2, width=8)

    def process():
        self.assertEqual((yield dut.w_rdy), 1)
        (yield dut.w_stb.eq(1))
        (yield dut.w_data.eq(170))
        (yield)
        self.assertEqual((yield dut.w_rdy), 1)
        (yield dut.w_stb.eq(1))
        (yield dut.w_lst.eq(1))
        (yield dut.w_drop.eq(1))
        (yield dut.w_data.eq(187))
        (yield)
        (yield)
        (yield Delay())
        self.assertEqual((yield dut.r_stb), 0)
    simulation_test(dut, process)
