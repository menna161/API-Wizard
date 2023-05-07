import os
import copy
import collections
import datetime
import six
import warnings
import numpy as np
import FlowCal.plot


def __new__(cls, infile):
    fcs_file = FCSFile(infile)
    if ('$TIMESTEP' in fcs_file.text):
        time_step = float(fcs_file.text['$TIMESTEP'])
    elif ('TIMETICKS' in fcs_file.text):
        time_step = (float(fcs_file.text['TIMETICKS']) / 1000.0)
    else:
        time_step = None
    data_type = fcs_file.text.get('$DATATYPE')
    acquisition_date = cls._parse_date_string(fcs_file.text.get('$DATE'))
    acquisition_start_time = cls._parse_time_string(fcs_file.text.get('$BTIM'))
    acquisition_end_time = cls._parse_time_string(fcs_file.text.get('$ETIM'))
    if (acquisition_date is not None):
        if (acquisition_start_time is not None):
            acquisition_start_time = datetime.datetime.combine(acquisition_date, acquisition_start_time)
        if (acquisition_end_time is not None):
            acquisition_end_time = datetime.datetime.combine(acquisition_date, acquisition_end_time)
    num_channels = int(fcs_file.text['$PAR'])
    channels = [fcs_file.text.get('$P{}N'.format(i)) for i in range(1, (num_channels + 1))]
    channels = tuple(channels)
    amplification_type = []
    for i in range(1, (num_channels + 1)):
        ati = fcs_file.text.get('$P{}E'.format(i))
        if (ati is not None):
            ati = ati.split(',')
            ati = [float(atij) for atij in ati]
            if ((ati[0] != 0.0) and (ati[1] == 0.0)):
                ati[1] = 1.0
            ati = tuple(ati)
        amplification_type.append(ati)
    amplification_type = tuple(amplification_type)
    data_range = []
    resolution = []
    for (ch_idx, ch) in enumerate(channels):
        PnR = float(fcs_file.text.get('$P{}R'.format((ch_idx + 1))))
        data_range.append([0.0, (PnR - 1)])
        resolution.append(int(PnR))
    resolution = tuple(resolution)
    detector_voltage = []
    for i in range(1, (num_channels + 1)):
        channel_detector_voltage = fcs_file.text.get('$P{}V'.format(i))
        if ((channel_detector_voltage is None) and ('CREATOR' in fcs_file.text) and ('CellQuest Pro' in fcs_file.text.get('CREATOR'))):
            channel_detector_voltage = fcs_file.text.get('BD$WORD{}'.format((12 + i)))
        if (channel_detector_voltage is not None):
            try:
                channel_detector_voltage = float(channel_detector_voltage)
            except ValueError:
                channel_detector_voltage = None
        detector_voltage.append(channel_detector_voltage)
    detector_voltage = tuple(detector_voltage)
    amplifier_gain = []
    for i in range(1, (num_channels + 1)):
        channel_amp_gain = fcs_file.text.get('$P{}G'.format(i))
        if ((channel_amp_gain is None) and ('CREATOR' in fcs_file.text) and ('FlowJoCollectorsEdition' in fcs_file.text.get('CREATOR'))):
            channel_amp_gain = fcs_file.text.get('CytekP{:02d}G'.format(i))
        if (channel_amp_gain is not None):
            try:
                channel_amp_gain = float(channel_amp_gain)
            except ValueError:
                channel_amp_gain = None
        amplifier_gain.append(channel_amp_gain)
    amplifier_gain = tuple(amplifier_gain)
    channel_labels = []
    for i in range(1, (num_channels + 1)):
        channel_label = fcs_file.text.get('$P{}S'.format(i), None)
        channel_labels.append(channel_label)
    channel_labels = tuple(channel_labels)
    data = fcs_file.data
    data.flags.writeable = True
    obj = data.view(cls)
    obj._infile = infile
    obj._text = fcs_file.text
    obj._analysis = fcs_file.analysis
    obj._data_type = data_type
    obj._time_step = time_step
    obj._acquisition_start_time = acquisition_start_time
    obj._acquisition_end_time = acquisition_end_time
    obj._channels = channels
    obj._amplification_type = amplification_type
    obj._detector_voltage = detector_voltage
    obj._amplifier_gain = amplifier_gain
    obj._channel_labels = channel_labels
    obj._range = data_range
    obj._resolution = resolution
    return obj
