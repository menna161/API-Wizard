import datetime
import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from tomlkit import loads


def parse_dict_nested(dictionary: Dict[(str, Dict[(str, tuple)])]) -> Any:
    "Parse nested dictionary.\n\n    Parameters\n    ----------\n    dictionary\n        The dictionary to parse like:\n            {'block': 'variable': (value, comment), ...}.\n\n    Returns\n    -------\n    date_time : datetime.datetime\n    header : list\n    block_names : list\n    (variables, values, comments, blocks) : Tuple[str, Any, str, str]\n    "
    blocks = list()
    variables = list()
    values = list()
    comments = list()
    header = None
    date_time = None
    for (key, item) in dictionary.items():
        if (key == '__header__'):
            header = item
        elif (key == '__datetime__'):
            date_time = item
        else:
            sub_dict = item
            for (sub_key, val) in sub_dict.items():
                variables.append(sub_key)
                values.append(val[0])
                comments.append(val[1])
                blocks.append(key)
    block_names = list(OrderedDict.fromkeys(blocks))
    return (date_time, header, block_names, (variables, values, comments, blocks))
