import argparse
import time
from math import pi
import matplotlib.pyplot as plt
import numpy as np
import senseact.devices.dxl.dxl_utils as dxl
import senseact.devices.dxl.dxl_mx64 as dxl_mx64


def read_time(driver, port, idn):
    " Read the entire control table of the DXL MX-64AT device 'N' times and plot the mean & percentile time taken. "
    times = []
    for i in range(1000):
        t1 = time.time()
        dxl.read_vals(driver, port, idn)
        times.append((time.time() - t1))
    print(np.mean(times))
    print(np.percentile(times, 99))
    plt.figure()
    plt.plot(times)
    plt.show()
