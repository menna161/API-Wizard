import datetime
import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from tomlkit import loads


def parse_dict_flat(dictionary: Dict) -> Any:
    "Parse flat dictionary.\n\n    Parameters\n    ----------\n    dictionary\n        The dictionary to parse like:\n            {'variable': [value, comment, block], ...}.\n\n    Returns\n    -------\n    date_time : datetime.datetime\n    header : list\n    block_names : list\n    (variables, values, comments, blocks) : Tuple[str, Any, str, str]\n    "
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
            var = key
            val = item[0]
            comment = item[1]
            block = item[2]
            variables.append(var)
            values.append(val)
            comments.append(comment)
            blocks.append(block)
    block_names = list(OrderedDict.fromkeys(blocks))
    return (date_time, header, block_names, (variables, values, comments, blocks))
