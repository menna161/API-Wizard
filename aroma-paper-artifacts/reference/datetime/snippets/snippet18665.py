import re
from datetime import datetime


def formatoutput(output, outtype='date'):
    '\n    format nasdaq datapoints to desired level - format dates, convert prices to numeric, etc.\n    :param output: output data\n    :param outtype: type of formatting\n    :return: formatted data point\n    '
    assert (outtype in ['date', 'price', 'volume']), 'formatout only supports date, price, volume\n                                                        \nUnsupported: {}'.format(outtype)
    if (outtype == 'date'):
        (tme, month, day, year) = output
        if (tme in ['', 'N/A', None]):
            return 'DATA NOT AVAILABLE'
        else:
            tme = filter_data(tme)
            return datetime.strptime('{}-{}-{} {}'.format(month, day, year, tme), '%m-%d-%Y %H:%M:%S %p')
    else:
        if (output in ['', 'N/A', None]):
            return 'DATA NOT AVAILABLE'
        if (outtype == 'price'):
            price = filter_data(output.replace('$', ''))
            return float(price)
        if (outtype == 'volume'):
            volume = filter_data(output)
            try:
                return float(volume)
            except ValueError:
                return volume
