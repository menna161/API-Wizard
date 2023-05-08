from .interface import Interface
from .common import filter_device_by_class, is_known_cmsis_dap_vid_pid
from ..dap_access_api import DAPAccessIntf
import logging
import os
import threading
import six
from time import sleep
import errno
import platform
import usb.core
import usb.util


@staticmethod
def get_all_connected_interfaces():
    '! @brief Returns all the connected devices with a CMSIS-DAPv2 interface.'
    try:
        all_devices = usb.core.find(find_all=True, custom_match=HasCmsisDapv2Interface())
    except usb.core.NoBackendError:
        return []
    boards = []
    for board in all_devices:
        new_board = PyUSBv2()
        new_board.vid = board.idVendor
        new_board.pid = board.idProduct
        new_board.product_name = board.product
        new_board.vendor_name = board.manufacturer
        new_board.serial_number = board.serial_number
        boards.append(new_board)
    return boards
