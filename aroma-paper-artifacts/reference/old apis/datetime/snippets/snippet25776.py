from alchemyjsonschema.custom.format import validate_time
from datetime import time
from datetime import time
from datetime import time
from datetime import time


def test_it4():
    from datetime import time
    now = (time(10, 20, 30).isoformat() + '.809840-10:20')
    result = _callFUT(now)
    assert (result is True)
