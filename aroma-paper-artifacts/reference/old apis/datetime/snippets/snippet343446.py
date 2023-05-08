from datetime import datetime
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.model.models as models
import archon.exchange.deribit.Wrapper as deribit
from datetime import datetime, timezone, timedelta


def show(sym):
    dt = datetime(2018, 12, 1)
    dt = dt.replace(tzinfo=timezone.utc)
    z = get_trades(sym, dt)
    for x in z:
        tsf = convert_time(x['timeStamp'])
        print(tsf, x['price'])
