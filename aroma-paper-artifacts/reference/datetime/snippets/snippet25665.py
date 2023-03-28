from alchemyjsonschema.custom.format import validate_date
from datetime import date


def test_it():
    from datetime import date
    print(date.today().isoformat())
    today = date.today().isoformat()
    result = _callFUT(today)
    assert (result is True)
