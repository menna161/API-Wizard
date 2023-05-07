import argparse
import time
from math import pi
import matplotlib.pyplot as plt
import numpy as np
import senseact.devices.dxl.dxl_utils as dxl
import senseact.devices.dxl.dxl_mx64 as dxl_mx64


def random_torque(driver, port, idn):
    " Read the entire control table and randomly sampled torque commands to the DXL.\n\n    This is done 'N' times and timed. Relevant data is plotted.\n    "
    dxl.write_torque_mode_enable(driver, port, idn, 1)
    times = []
    vals_dict = {'present_pos': ((2 * pi) / 3.0), 'current': 0}
    actions = []
    currents = []
    for i in range(1000):
        t1 = time.time()
        if (vals_dict['present_pos'] < (pi / 3.0)):
            action = 1000
            dxl.write_torque(driver, port, idn, action)
            time.sleep(0.001)
        elif (vals_dict['present_pos'] > pi):
            action = (- 1000)
            dxl.write_torque(driver, port, idn, action)
            time.sleep(0.001)
        else:
            action = int((np.random.uniform((- 1), 1) * 1000))
        dxl.write_torque(driver, port, idn, action)
        vals_dict = dxl.read_vals(driver, port, idn)
        actions.append(action)
        currents.append(vals_dict['current'])
        times.append((time.time() - t1))
    dxl.write_torque(driver, port, idn, 0)
    print(np.mean(times))
    print(currents[:10])
    plt.xcorr(currents, actions)
    plt.figure()
    plt.plot(np.cumsum(times), actions, label='actions')
    plt.plot(np.cumsum(times), currents, label='currents')
    plt.legend()
    plt.figure()
    plt.plot(times)
    plt.show()
