import datetime
import doctest


def __write_rnx3_header_runby__(pgm='Rokubun', agency='not-available'):
    '\n    Write the runby header line of the Rinex file\n    '
    TAIL = 'PGM / RUN BY / DATE'
    datestr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    res = '{0:20s}{1:20s}{2:20s}{3}\n'.format(pgm, agency, datestr, TAIL)
    return res
