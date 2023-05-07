import traces
import random


def test_compact():
    for n_trial in range(100):
        test_ts = traces.TimeSeries()
        compact_ts = traces.TimeSeries()
        for t in range(100):
            value = random.randint(0, 2)
            test_ts.set(t, value)
            compact_ts.set(t, value, compact=True)
        test_ts.compact()
        assert (test_ts.items() == compact_ts.items())
