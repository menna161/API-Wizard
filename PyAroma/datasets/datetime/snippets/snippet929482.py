import datetime
import nose
from traces import TimeSeries
from traces.decorators import ignorant, strict


def example_mean():
    ts = TimeSeries()
    ts[datetime.datetime(2010, 1, 1)] = 0
    ts[datetime.datetime(2010, 1, 3, 10)] = 1
    ts[datetime.datetime(2010, 1, 5)] = 0
    ts[datetime.datetime(2010, 1, 8)] = 1
    ts[datetime.datetime(2010, 1, 17)] = 0
    ts[datetime.datetime(2010, 1, 19)] = 1
    ts[datetime.datetime(2010, 1, 23)] = 0
    ts[datetime.datetime(2010, 1, 26)] = 1
    ts[datetime.datetime(2010, 1, 28)] = 0
    ts[datetime.datetime(2010, 1, 31)] = 1
    ts[datetime.datetime(2010, 2, 5)] = 0
    for (time, value) in ts:
        print(time.isoformat(), ((0.1 * value) + 1.1))
    print('')
    timestep = {'hours': 25}
    start = datetime.datetime(2010, 1, 1)
    while (start <= datetime.datetime(2010, 2, 5)):
        end = (start + datetime.timedelta(**timestep))
        print(start.isoformat(), ts.mean(start, end))
        start = end
    print('')
    start = datetime.datetime(2010, 1, 1)
    while (start <= datetime.datetime(2010, 2, 5)):
        end = (start + datetime.timedelta(**timestep))
        print(start.isoformat(), (- 0.2))
        print(start.isoformat(), 1.2)
        start = end
