import sys
import glob
from datetime import datetime, timedelta
import traces
from traces.utils import datetime_range


def read_all(pattern='data/lightbulb-*.csv'):
    'Read all of the CSVs in a directory matching the filename pattern\n    as TimeSeries.\n\n    '
    result = []
    for filename in glob.iglob(pattern):
        print('reading', filename, file=sys.stderr)
        ts = traces.TimeSeries.from_csv(filename, time_column=0, time_transform=parse_iso_datetime, value_column=1, value_transform=int, default=0)
        ts.compact()
        result.append(ts)
    return result
