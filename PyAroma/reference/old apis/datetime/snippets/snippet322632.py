import datetime
import math
import re
import sys
import doctest


def process(measurement, fullbiasnanos=None, integerize=False, pseudorange_bias=0.0, filter_mode='sync'):
    '\n    Process a log measurement. This method computes the pseudorange, carrier-phase (in cycles)\n    Doppler (cycles/s) as well as CN/0\n\n    :param measurement: GNSS Logger measurement line to process\n    :param fullbiasnanos: Full Bias Nanos, used to either fix it to a certain\n                          value (if value is provided) or update it with the\n                          data if None (default value)\n    :param integerize: Boolean to control whether to integerize the measurements\n                       to the nearest "integerized" time stamp (in this case\n                       to the nearest second)\n    :param pseudorange_bias: Add an externally computed bias to the pseudorange.\n                             Default is 0.0\n    :param filter_mode: Specify the filtering scheme for the raw file. Acceptable values are\n                        sync: TOW/TOD known, code locked, no ambiguities are\n                        detected, and all remaining flags for the signal are set\n                        trck: TOW/TOD known, code locked and no ambiguities are detected\n    '
    try:
        satname = get_satname(measurement)
    except ValueError as e:
        sys.stderr.write('{0}\n'.format(e))
        return None
    obscode = get_obscode(measurement)
    fullbiasnanos = (measurement['FullBiasNanos'] if (fullbiasnanos is None) else fullbiasnanos)
    try:
        timenanos = float(measurement['TimeNanos'])
    except ValueError:
        raise ValueError('-- WARNING: Invalid value of TimeNanos or satellite  [ {0} ]\n'.format(satname))
    try:
        biasnanos = float(measurement['BiasNanos'])
    except ValueError:
        biasnanos = 0.0
    gpsweek = math.floor((((- fullbiasnanos) * NS_TO_S) / GPS_WEEKSECS))
    local_est_GPS_time = (timenanos - (fullbiasnanos + biasnanos))
    gpssow = ((local_est_GPS_time * NS_TO_S) - (gpsweek * GPS_WEEKSECS))
    frac = ((gpssow - int((gpssow + 0.5))) if integerize else 0.0)
    gpst_epoch = (GPSTIME + datetime.timedelta(weeks=gpsweek, seconds=(gpssow - frac)))
    try:
        timeoffsetnanos = float(measurement['TimeOffsetNanos'])
    except ValueError:
        timeoffsetnanos = 0.0
    tRxSeconds = (gpssow - (timeoffsetnanos * NS_TO_S))
    wavelength = (SPEED_OF_LIGHT / get_frequency(measurement))
    try:
        if (filter_mode == 'sync'):
            check_sync_state(measurement)
        elif (filter_mode == 'trck'):
            check_trck_state(measurement)
        else:
            raise ValueError('-- ERROR: Invalid value of --filter-mode option')
    except ValueError as e:
        sys.stderr.write('-- WARNING: {0} for satellite [ {1} ]\n'.format(e, satname))
        range = 0
    else:
        constellation = measurement['ConstellationType']
        if (constellation == CONSTELLATION_GLONASS):
            tod_secs = (measurement['ReceivedSvTimeNanos'] * NS_TO_S)
            tTxSeconds = glot_to_gpst(gpst_epoch, tod_secs)
            tau = check_week_crossover(tRxSeconds, tTxSeconds)
        elif (constellation == CONSTELLATION_BEIDOU):
            tTxSeconds = ((measurement['ReceivedSvTimeNanos'] * NS_TO_S) + BDST_TO_GPST)
            tau = check_week_crossover(tRxSeconds, tTxSeconds)
        else:
            tTxSeconds = (measurement['ReceivedSvTimeNanos'] * NS_TO_S)
            tau = check_week_crossover(tRxSeconds, tTxSeconds)
        range = ((tau * SPEED_OF_LIGHT) - pseudorange_bias)
        if integerize:
            range -= (frac * measurement['PseudorangeRateMetersPerSecond'])
    try:
        check_adr_state(measurement)
    except ValueError as e:
        sys.stderr.write('-- WARNING: {0} for satellite [ {1} ]\n'.format(e, satname))
        cphase = 0
    else:
        cphase = (measurement['AccumulatedDeltaRangeMeters'] / wavelength)
    doppler = ((- measurement['PseudorangeRateMetersPerSecond']) / wavelength)
    cn0 = measurement['Cn0DbHz']
    return {EPOCH_STR: gpst_epoch, satname: {('C' + obscode): range, ('L' + obscode): cphase, ('D' + obscode): doppler, ('S' + obscode): cn0}}
