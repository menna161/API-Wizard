import numpy as np
import scipy
from scipy import integrate
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import integrate
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import integrate
import matplotlib.pyplot as plt


def icecore_diffuse(d18O, b, time, T, P, depth, depth_horizons, dz, drho):
    '\n        DOCSTRING: Function \'icecore_diffuse\'\n        DESCRIPTION: accounts for diffusion and compaction in the firn.\n\n        Inputs:\n            d18O: ice core isotope ratio, output from sensor Model (permil)\n            b   : average accumulation rate at site (m/year)\n            time: calendar years of record\n            T   : average temperature at site (K)\n            P   : average sea level pressure at site (atm)\n            depth: total depth of core\n            depth_horizons: accumulation by year in ice core--depth horizons (moving downwards in core) in meters\n            dz: step in depth (default = min(depth_horizons)/10.) \n            drho: step in density (default=0.5 kg/m^3)\n\n        Diffusion is computed using a convolution (Gaussian smoothing).\n\n        Functionality: Calculates diffusion length as a function of density\n        in firn, and given vectors of time-depth and density-depth \n        Also expects Pressure in atm, T in K, rho and rho_ice in \n        kg/m^3, but defaults on these, so only the first three arguments\n        must be entered.\n\n        "Time" is really "age" (increasing down core) and is given in years.\n        z is depth in meters\n        rho should be in kg/m^3\n        the vectors rho, time, and z should all correponding with one another\n    '
    import numpy as np
    import scipy
    from scipy import integrate
    import matplotlib.pyplot as plt
    R = 8.314478
    m = 0.01802
    rho_s = 300.0
    rho_d = 822.0
    rho_i = 920.0
    z = (np.arange(0, depth, dz) + dz)
    (rho, zieq, t) = densification(T, b, rho_s, z)
    rho = rho[0:len(z)]
    time_d = np.cumsum((((dz / b) * rho) / rho_i))
    ts = (((time_d * 365.25) * 24) * 3600)
    drho = np.diff(rho)
    dtdrho = (np.diff(ts) / np.diff(rho))
    D = diffusivity(rho, T, P, rho_d, b)
    D = D[0:(- 1)]
    rho = rho[0:(- 1)]
    diffs = (np.diff(z) / np.diff(time_d))
    diffs = diffs[0:(- 1)]
    solidice = np.where((rho >= (rho_d - 5.0)))
    diffusion = np.where((rho < (rho_d - 5.0)))
    sigma_sqrd_dummy = ((((2 * np.power(rho, 2)) * dtdrho) * D) * drho)
    sigma_sqrd = integrate.cumtrapz(sigma_sqrd_dummy)
    rho = rho[0:(- 1)]
    sigma = np.zeros((len(rho) + 1))
    sigma[diffusion] = np.sqrt(((1 / np.power(rho, 2)) * sigma_sqrd))
    sigma[solidice] = sigma[diffusion][(- 1)]
    sigma = sigma[0:(- 1)]
    del18 = np.flipud(d18O)
    depth_horizons = depth_horizons
    years_rev = np.flipud(time)
    z = np.reshape(z, len(z))
    del18 = np.reshape(del18, len(del18))
    iso_interp = np.interp(z, depth_horizons, del18)
    time_interp = np.interp(z, depth_horizons, years_rev)
    diffused_final = np.zeros(len(iso_interp))
    zp = np.arange((- 100), 100, dz)
    if (len(zp) >= (0.5 * len(z))):
        print('Warning: convolution kernal length (zp) is approaching that of half the length of timeseries. Kernal being clipped.')
        bound = ((0.2 * len(z)) * dz)
        zp = np.arange((- bound), bound, dz)
    sigma_dummy = np.tile(0.08, len(sigma))
    for i in range(len(sigma)):
        part1 = (1.0 / (sigma[i] * np.sqrt((2.0 * np.pi))))
        part2 = scipy.exp(((- (zp ** 2)) / (2 * (sigma[i] ** 2))))
        G = (part1 * part2)
        rm = np.mean(iso_interp)
        cdel = (iso_interp - rm)
        diffused = (np.convolve(G, cdel, mode='same') * dz)
        diffused = (diffused + rm)
        diffused_final[i] = diffused[i]
    diffused_timeseries = diffused_final[0:(- 3)]
    final_iso = np.interp(depth_horizons, z[0:(- 3)], diffused_timeseries)
    ice_diffused = final_iso
    return (z, sigma, D, time_d, diffs, ice_diffused, rho, zieq)
