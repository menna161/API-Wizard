import binascii
import datetime
from bitstring import BitArray


def encodeValue(data, forDict=False):
    final_data = BitArray()
    if (data is None):
        final_data.append('int:8=0')
    elif isinstance(data, bool):
        final_data.append('int:8=1')
        final_data.append(f'int:8={int(data)}')
    elif isinstance(data, int):
        if (data > 2147483647):
            final_data.append('int:8=3')
            final_data.append(f'int:64={data}')
        else:
            final_data.append('int:8=2')
            final_data.append(f'int:32={data}')
    elif isinstance(data, float):
        final_data.append('int:8=4')
        final_data.append(f'float:64={data}')
    elif isinstance(data, str):
        if (not forDict):
            final_data.append('int:8=5')
        if (not all(((ord(c) < 128) for c in data))):
            length = (len(data.encode().hex()) // 2)
        else:
            length = len(data)
        while ((length & 4294967168) != 0):
            final_data.append(f'uint:8={((length & 127) | 128)}')
            length = zero_fill_right_shift(length, 7)
        final_data.append(f'uint:8={(length & 127)}')
        final_data.append(data.encode())
    elif isinstance(data, dict):
        final_data.append('int:8=6')
        final_data.append(encodeDictionary(data))
    elif isinstance(data, list):
        final_data.append('int:8=7')
        final_data.append(encodeArray(data))
    elif isinstance(data, datetime.datetime):
        final_data.append('int:8=8')
        final_data.append(f'int:64={int((data.timestamp() * 1000))}')
    else:
        raise ValueError(("Can't encode " + str(type(data))))
    return final_data
