from .interface import Interface
from .common import filter_device_by_class, is_known_cmsis_dap_vid_pid
from ..dap_access_api import DAPAccessIntf
import logging
import os
import threading
import six
from time import sleep
import platform
import errno
import usb.core
import usb.util


@staticmethod
def get_all_connected_interfaces():
    '\n        returns all the connected devices which matches PyUSB.vid/PyUSB.pid.\n        returns an array of PyUSB (Interface) objects\n        '
    all_devices = usb.core.find(find_all=True, custom_match=FindDap())
    boards = []
    for board in all_devices:
        new_board = PyUSB()
        new_board.vid = board.idVendor
        new_board.pid = board.idProduct
        new_board.product_name = board.product
        new_board.vendor_name = board.manufacturer
        new_board.serial_number = board.serial_number
        boards.append(new_board)
    return boards
