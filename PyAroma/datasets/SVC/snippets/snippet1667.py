from ..core.target import Target
from ..core import exceptions
from ..utility import cmdline, conversion, timeout
from ..utility.notification import Notification
from .component import CoreSightComponent
from .fpb import FPB
from .dwt import DWT
from ..debug.breakpoints.manager import BreakpointManager
from ..debug.breakpoints.software import SoftwareBreakpointProvider
import logging
from time import time, sleep
from xml.etree.ElementTree import Element, SubElement, tostring


def _perform_emulated_reset(self):
    '! @brief Emulate a software reset by writing registers.\n        \n        All core registers are written to reset values. This includes setting the initial PC and SP\n        to values read from the vector table, which is assumed to be located at the based of the\n        boot memory region.\n        \n        If the memory map does not provide a boot region, then the current value of the VTOR register\n        is reused, as it should at least point to a valid vector table.\n        \n        The current value of DEMCR.VC_CORERESET determines whether the core will be resumed or\n        left halted.\n        \n        Note that this reset method will not set DHCSR.S_RESET_ST or DFSR.VCATCH.\n        '
    self.halt()
    bootMemory = self.memory_map.get_boot_memory()
    if (bootMemory is None):
        vectorBase = self.read32(self.VTOR)
    else:
        vectorBase = bootMemory.start
    initialSp = self.read32(vectorBase)
    initialPc = self.read32((vectorBase + 4))
    regList = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'psp', 'msp', 'lr', 'pc', 'xpsr', 'cfbp']
    valueList = (([0] * 13) + [0, initialSp, 4294967295, initialPc, 16777216, 0])
    if self.has_fpu:
        regList += ([('s%d' % n) for n in range(32)] + ['fpscr'])
        valueList += ([0] * 33)
    self.write_core_registers_raw(regList, valueList)
    data = [(self.ICSR_PENDSVCLR | self.ICSR_PENDSTCLR), vectorBase, (self.NVIC_AIRCR_VECTKEY | self.NVIC_AIRCR_VECTCLRACTIVE), 0, 0, 0, 0, 0, 0, 0]
    self.write_memory_block32(self.ICSR, data)
    self.write32(self.CPACR, 0)
    if self.has_fpu:
        data = [0, 0, 0]
        self.write_memory_block32(self.FPCCR, data)
    self.write_memory_block32(self.SYSTICK_CSR, ([0] * 3))
    numregs = ((self.read32(self.ICTR) & 15) + 1)
    self.write_memory_block32(self.NVIC_ICER0, ([4294967295] * numregs))
    self.write_memory_block32(self.NVIC_ICPR0, ([4294967295] * numregs))
    self.write_memory_block32(self.NVIC_IPR0, ([4294967295] * (numregs * 8)))
