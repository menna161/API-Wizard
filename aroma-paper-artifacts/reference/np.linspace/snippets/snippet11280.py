import numpy as np


def porosity(depth_profile):
    import numpy as np
    z = np.linspace(0, depth_profile, num=100)
    ps = 2650.0
    pw = 1000.0
    g = 9.8
    phi = np.zeros(len(z))
    phi_0 = 0.95
    k1 = ((1 - phi_0) / phi_0)
    c = 3.68e-08
    for i in range(len(phi)):
        phi[i] = (np.exp(((((- c) * g) * (ps - pw)) * z[i])) / (np.exp(((((- c) * g) * (ps - pw)) * z[i])) + k1))
    return (phi, z)
