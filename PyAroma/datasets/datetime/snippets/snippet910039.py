import os
import copy
import collections
import datetime
import six
import warnings
import numpy as np
import FlowCal.plot


def read_fcs_data_segment(buf, begin, end, datatype, num_events, param_bit_widths, big_endian, param_ranges=None):
    '\n    Read DATA segment of FCS file.\n\n    Parameters\n    ----------\n    buf : file-like object\n        Buffer containing data to interpret as DATA segment.\n    begin : int\n        Offset (in bytes) to first byte of DATA segment in `buf`.\n    end : int\n        Offset (in bytes) to last byte of DATA segment in `buf`.\n    datatype : {\'I\', \'F\', \'D\', \'A\'}\n        String specifying FCS file datatype (see $DATATYPE keyword from\n        FCS standards). Supported datatypes include \'I\' (unsigned\n        binary integer), \'F\' (single precision floating point), and \'D\'\n        (double precision floating point). \'A\' (ASCII) is recognized\n        but not supported.\n    num_events : int\n        Total number of events (see $TOT keyword from FCS standards).\n    param_bit_widths : array-like\n        Array specifying parameter (aka channel) bit width for each\n        parameter (see $PnB keywords from FCS standards). The length of\n        `param_bit_widths` should match the $PAR keyword value from the\n        FCS standards (which indicates the total number of parameters).\n        If `datatype` is \'I\', data must be byte aligned (i.e. all\n        parameter bit widths should be divisible by 8), and data are\n        upcast to the nearest uint8, uint16, uint32, or uint64 data\n        type. Bit widths larger than 64 bits are not supported.\n    big_endian : bool\n        Endianness of computer used to acquire data (see $BYTEORD\n        keyword from FCS standards). True implies big endian; False\n        implies little endian.\n    param_ranges : array-like, optional\n        Array specifying parameter (aka channel) range for each\n        parameter (see $PnR keywords from FCS standards). Used to\n        ensure erroneous values are not read from DATA segment by\n        applying a bit mask to remove unused bits. The length of\n        `param_ranges` should match the $PAR keyword value from the FCS\n        standards (which indicates the total number of parameters). If\n        None, no masking is performed.\n\n    Returns\n    -------\n    data : numpy array\n        NxD numpy array describing N cytometry events observing D data\n        dimensions.\n\n    Raises\n    ------\n    ValueError\n        If lengths of `param_bit_widths` and `param_ranges` don\'t match.\n    ValueError\n        If calculated DATA segment size (as determined from the number\n        of events, the number of parameters, and the number of bytes per\n        data point) does not match size specified by `begin` and `end`.\n    ValueError\n        If `param_bit_widths` doesn\'t agree with `datatype` for single\n        precision or double precision floating point (i.e. they should\n        all be 32 or 64, respectively).\n    ValueError\n        If `datatype` is unrecognized.\n    NotImplementedError\n        If `datatype` is \'A\'.\n    NotImplementedError\n        If `datatype` is \'I\' but data is not byte aligned.\n\n    References\n    ----------\n    .. [1] P.N. Dean, C.B. Bagwell, T. Lindmo, R.F. Murphy, G.C. Salzman,\n       "Data file standard for flow cytometry. Data File Standards\n       Committee of the Society for Analytical Cytology," Cytometry vol\n       11, pp 323-332, 1990, PMID 2340769.\n\n    .. [2] L.C. Seamer, C.B. Bagwell, L. Barden, D. Redelman, G.C. Salzman,\n       J.C. Wood, R.F. Murphy, "Proposed new data file standard for flow\n       cytometry, version FCS 3.0," Cytometry vol 28, pp 118-122, 1997,\n       PMID 9181300.\n\n    .. [3] J. Spidlen, et al, "Data File Standard for Flow Cytometry,\n       version FCS 3.1," Cytometry A vol 77A, pp 97-100, 2009, PMID\n       19937951.\n\n    '
    num_params = len(param_bit_widths)
    if ((param_ranges is not None) and (len(param_ranges) != num_params)):
        raise ValueError(('param_bit_widths and param_ranges must have same' + ' length'))
    shape = (int(num_events), num_params)
    if (datatype == 'I'):
        if (all(((bw == 8) for bw in param_bit_widths)) or all(((bw == 16) for bw in param_bit_widths)) or all(((bw == 32) for bw in param_bit_widths)) or all(((bw == 64) for bw in param_bit_widths))):
            num_bits = param_bit_widths[0]
            if ((((shape[0] * shape[1]) * (num_bits // 8)) != ((end + 1) - begin)) and (((shape[0] * shape[1]) * (num_bits // 8)) != (end - begin))):
                raise ValueError(((('DATA size does not match expected array' + ' size (array size =') + ' {0} bytes,'.format(((shape[0] * shape[1]) * (num_bits // 8)))) + ' DATA segment size = {0} bytes)'.format(((end + 1) - begin))))
            dtype = np.dtype('{0}u{1}'.format(('>' if big_endian else '<'), (num_bits // 8)))
            data = np.memmap(buf, dtype=dtype, mode='r', offset=begin, shape=shape, order='C')
            data = np.array(data)
        else:
            if ((not all((((bw % 8) == 0) for bw in param_bit_widths))) or any(((bw > 64) for bw in param_bit_widths))):
                raise NotImplementedError((('only byte aligned parameter bit' + ' widths (bw % 8 = 0) <= 64 are supported') + ' (param_bit_widths={0})'.format(param_bit_widths)))
            byte_shape = (int(num_events), np.sum((np.array(param_bit_widths) // 8)))
            if (((byte_shape[0] * byte_shape[1]) != ((end + 1) - begin)) and ((byte_shape[0] * byte_shape[1]) != (end - begin))):
                raise ValueError(((('DATA size does not match expected array' + ' size (array size =') + ' {0} bytes,'.format((byte_shape[0] * byte_shape[1]))) + ' DATA segment size = {0} bytes)'.format(((end + 1) - begin))))
            byte_data = np.memmap(buf, dtype='uint8', mode='r', offset=begin, shape=byte_shape, order='C')
            upcast_bw = int((2 ** np.max(np.ceil(np.log2(param_bit_widths)))))
            upcast_dtype = 'u{0}'.format((upcast_bw // 8))
            data = np.zeros(shape, dtype=upcast_dtype)
            byte_boundaries = np.roll((np.cumsum(param_bit_widths) // 8), 1)
            byte_boundaries[0] = 0
            for col in range(data.shape[1]):
                num_bytes = (param_bit_widths[col] // 8)
                for b in range(num_bytes):
                    byte_data_col = (byte_boundaries[col] + b)
                    byteshift = (((num_bytes - b) - 1) if big_endian else b)
                    if (byteshift > 0):
                        data[(:, col)] += (byte_data[(:, byte_data_col)].astype(upcast_dtype) << (byteshift * 8))
                    else:
                        data[(:, col)] += byte_data[(:, byte_data_col)]
        if (param_ranges is not None):
            for col in range(data.shape[1]):
                bits_used = int(np.ceil(np.log2(param_ranges[col])))
                bitmask = (~ ((~ 0) << bits_used))
                data[(:, col)] &= bitmask
    elif (datatype in ('F', 'D')):
        num_bits = (32 if (datatype == 'F') else 64)
        if (not all(((bw == num_bits) for bw in param_bit_widths))):
            raise ValueError(((('all param_bit_widths should be' + ' {0} if datatype ='.format(num_bits)) + " '{0}' (param_bit_widths=".format(datatype)) + '{0})'.format(param_bit_widths)))
        if ((((shape[0] * shape[1]) * (num_bits // 8)) != ((end + 1) - begin)) and (((shape[0] * shape[1]) * (num_bits // 8)) != (end - begin))):
            raise ValueError(((('DATA size does not match expected array size' + ' (array size = {0}'.format(((shape[0] * shape[1]) * (num_bits // 8)))) + ' bytes, DATA segment size =') + ' {0} bytes)'.format(((end + 1) - begin))))
        dtype = np.dtype('{0}f{1}'.format(('>' if big_endian else '<'), (num_bits // 8)))
        data = np.memmap(buf, dtype=dtype, mode='r', offset=begin, shape=shape, order='C')
        data = np.array(data)
    elif (datatype == 'A'):
        raise NotImplementedError(((("only 'I' (unsigned binary integer)," + " 'F' (single precision floating point), and 'D' (double") + ' precision floating point) data types are supported (detected') + " datatype='{0}')".format(datatype)))
    else:
        raise ValueError(('unrecognized datatype (detected datatype=' + "'{0}')".format(datatype)))
    return data
