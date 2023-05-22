import datetime
import nose
from traces import TimeSeries
from traces.decorators import ignorant, strict


def example_dictlike():
    ts = TimeSeries()
    ts[datetime.datetime(2010, 1, 1)] = 5
    ts[datetime.datetime(2010, 1, 2)] = 4
    ts[datetime.datetime(2010, 1, 3)] = 3
    ts[datetime.datetime(2010, 1, 7)] = 2
    ts[datetime.datetime(2010, 1, 4)] = 1
    ts[datetime.datetime(2010, 1, 4)] = 10
    ts[datetime.datetime(2010, 1, 4)] = 5
    ts[datetime.datetime(2010, 1, 1)] = 1
    ts[datetime.datetime(2010, 1, 7)] = 1.2
    ts[datetime.datetime(2010, 1, 8)] = 1.3
    ts[datetime.datetime(2010, 1, 12)] = 1.3
    dt = datetime.datetime(2010, 1, 12)
    for i in range(1000):
        dt += datetime.timedelta(hours=random.random())
        ts[dt] = math.sin((i / float(math.pi)))
    dt -= datetime.timedelta(hours=500)
    dt -= datetime.timedelta(minutes=30)
    for i in range(1000):
        dt += datetime.timedelta(hours=random.random())
        ts[dt] = math.cos((i / float(math.pi)))
    for (i, j) in ts:
        print(i.isoformat(), j)
