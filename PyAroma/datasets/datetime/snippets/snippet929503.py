from datetime import datetime
import pickle
import nose
from traces import TimeSeries
import csv
import os


def test_csv():

    def time_parse(value):
        return int(value)

    def value_parse(value):
        try:
            return int(value)
        except ValueError:
            return None
    filename = 'sample.csv'
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['hour', 'value'])
        writer.writerow(['10', '15'])
        writer.writerow(['11', '34'])
        writer.writerow(['12', '19'])
        writer.writerow(['13', 'nan'])
        writer.writerow(['14', '18'])
        writer.writerow(['15', 'nan'])
    ts = TimeSeries.from_csv(filename, time_column=0, time_transform=time_parse, value_column=1, value_transform=value_parse, default=None)
    os.remove(filename)
    assert (ts[9] is None)
    assert (ts[20] is None)
    assert (ts[13.5] is None)
    histogram = ts.distribution()
    nose.tools.assert_almost_equal(histogram.mean(), ((((15 + 34) + 19) + 18) / 4.0))
    filename = 'sample.csv'
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['hour', 'value'])
        writer.writerow(['2000-01-01 10:00:00', '15'])
        writer.writerow(['2000-01-01 11:00:00', '34'])
        writer.writerow(['2000-01-01 12:00:00', '19'])
        writer.writerow(['2000-01-01 13:00:00', 'nan'])
        writer.writerow(['2000-01-01 14:00:00', '18'])
        writer.writerow(['2000-01-01 15:00:00', 'nan'])
    ts = TimeSeries.from_csv(filename)
    os.remove(filename)
    assert (ts[datetime(2000, 1, 1, 9)] is None)
    assert (ts[datetime(2000, 1, 1, 10, 30)] == '15')
    assert (ts[datetime(2000, 1, 1, 20)] == 'nan')
