from .interface import Interface
from .common import filter_device_by_usage_page
from ..dap_access_api import DAPAccessIntf
from ....utility.timeout import Timeout
import logging
import os
import collections
from time import time, sleep
import six
import pywinusb.hid as hid


@staticmethod
def get_all_connected_interfaces():
    '\n        returns all the connected CMSIS-DAP devices\n        '
    all_devices = hid.find_all_hid_devices()
    all_mbed_devices = []
    for d in all_devices:
        if (d.product_name.find('CMSIS-DAP') >= 0):
            all_mbed_devices.append(d)
    boards = []
    for dev in all_mbed_devices:
        try:
            dev.open(shared=True)
            if filter_device_by_usage_page(dev.vendor_id, dev.product_id, dev.hid_caps.usage_page):
                dev.close()
                continue
            report = dev.find_output_reports()
            if (len(report) != 1):
                dev.close()
                continue
            new_board = PyWinUSB()
            new_board.report = report[0]
            new_board.vendor_name = dev.vendor_name
            new_board.product_name = dev.product_name
            new_board.serial_number = dev.serial_number
            new_board.vid = dev.vendor_id
            new_board.pid = dev.product_id
            new_board.device = dev
            dev.close()
            boards.append(new_board)
        except Exception as e:
            if (str(e) != 'Failure to get HID pre parsed data'):
                log.error('Receiving Exception: %s', e)
            dev.close()
    return boards
