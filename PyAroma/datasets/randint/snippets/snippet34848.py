import argparse
import time
from math import pi
import matplotlib.pyplot as plt
import numpy as np
import senseact.devices.dxl.dxl_utils as dxl
import senseact.devices.dxl.dxl_mx64 as dxl_mx64


def sync_write_test(driver, port, dxl_ids):
    ' Performs synchronized write operations to a target register in multiple DXLs.\n\n    NOTE: Valid only on select DXL models.\n\n    Args:\n        dxl_ids: A list of ints containing DXL id numbers\n    '
    if driver.is_ctypes_driver:
        count = len(dxl_ids)
        goals = ([np.random.randint(0, 2000)] * count)
        joint_mode_block = dxl_mx64.MX64.subblock('torque_control_mode_enable', 'torque_control_mode_enable', ret_dxl_type=True)
        driver.sync_write(port, joint_mode_block, zip(dxl_ids, ([0] * count)))
        low_angle_limit_block = dxl_mx64.MX64.subblock('angle_limit_cw', 'angle_limit_cw', ret_dxl_type=True)
        driver.sync_write(port, low_angle_limit_block, zip(dxl_ids, ([0] * count)))
        high_angle_limit_block = dxl_mx64.MX64.subblock('angle_limit_ccw', 'angle_limit_ccw', ret_dxl_type=True)
        driver.sync_write(port, high_angle_limit_block, zip(dxl_ids, ([2048] * count)))
        speed_block = dxl_mx64.MX64.subblock('moving_speed', 'moving_speed', ret_dxl_type=True)
        driver.sync_write(port, speed_block, zip(dxl_ids, ([1000] * count)))
        goal_block = dxl_mx64.MX64.subblock('goal_pos', 'goal_pos', ret_dxl_type=True)
        read_block = dxl_mx64.MX64.subblock('version_0', 'goal_acceleration', ret_dxl_type=True)
        data = zip(dxl_ids, goals)
        driver.sync_write(port, goal_block, data)
        for i in range(100):
            for id in dxl_ids:
                vals_dict = driver.read_a_block(port, id, read_block, read_wait_time=0.0001)
                print(id, vals_dict['goal_pos'], vals_dict['present_pos'])
