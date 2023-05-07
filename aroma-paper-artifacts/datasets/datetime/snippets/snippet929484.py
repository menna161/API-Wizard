import datetime
import nose
from traces import TimeSeries
from traces.decorators import ignorant, strict


def example_sum():
    a = TimeSeries()
    a.set(datetime.datetime(2015, 3, 1), 1)
    a.set(datetime.datetime(2015, 3, 2), 0)
    a.set(datetime.datetime(2015, 3, 3), 1)
    a.set(datetime.datetime(2015, 3, 5), 0)
    a.set(datetime.datetime(2015, 3, 6), 0)
    b = TimeSeries()
    b.set(datetime.datetime(2015, 3, 1), 0)
    b.set(datetime.datetime(2015, 3, 2, 12), 1)
    b.set(datetime.datetime(2015, 3, 3, 13, 13), 0)
    b.set(datetime.datetime(2015, 3, 4), 1)
    b.set(datetime.datetime(2015, 3, 5), 0)
    b.set(datetime.datetime(2015, 3, 5, 12), 1)
    b.set(datetime.datetime(2015, 3, 5, 19), 0)
    c = TimeSeries()
    c.set(datetime.datetime(2015, 3, 1, 17), 0)
    c.set(datetime.datetime(2015, 3, 1, 21), 1)
    c.set(datetime.datetime(2015, 3, 2, 13, 13), 0)
    c.set(datetime.datetime(2015, 3, 4, 18), 1)
    c.set(datetime.datetime(2015, 3, 5, 4), 0)
    for (i, ts) in enumerate([a, b, c]):
        for ((t0, v0), (t1, v1)) in ts.iterintervals(1):
            print(t0.isoformat(), i)
            print(t1.isoformat(), i)
        print('')
        for ((t0, v0), (t1, v1)) in ts.iterintervals(0):
            print(t0.isoformat(), i)
            print(t1.isoformat(), i)
        print('')
    for (dt, i) in TimeSeries.merge([a, b, c], operation=sum):
        print(dt.isoformat(), i)
