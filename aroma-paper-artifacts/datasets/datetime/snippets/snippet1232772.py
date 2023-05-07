import datetime
import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from tomlkit import loads


def parse_json_file(filepath: Union[(str, Path)]) -> Any:
    'Parse JSON config file.\n\n    Parameters\n    ----------\n    filepath\n        The file name or path to the JSON file.\n\n    Returns\n    -------\n    date_time : datetime.datetime\n    header : list\n    block_names : list\n    (variables, values, comments, blocks) : Tuple[str, Any, str, str]\n    '
    with open(filepath, mode='r') as fp:
        json_dict = json.load(fp)
    blocks = list()
    variables = list()
    values = list()
    comments = list()
    header = None
    date_time = None
    for (key, item) in json_dict.items():
        if (key in ['__header__', 'header']):
            header = item
        elif (key in ['__datetime__', 'datetime']):
            date_time = datetime.datetime.strptime(item, '%d/%m/%Y %H:%M:%S.%f')
        else:
            for (var, val, comment) in item:
                if isinstance(val, str):
                    if re.fullmatch('\\d\\d\\d:\\d\\d', val):
                        val = val.split(':')
                        val = datetime.timedelta(hours=int(val[0]), minutes=int(val[1]))
                variables.append(var)
                values.append(val)
                comments.append(comment)
                blocks.append(key)
    block_names = list(json_dict.keys())
    try:
        block_names.remove('__header__')
    except ValueError:
        pass
    try:
        block_names.remove('__datetime__')
    except ValueError:
        pass
    return (date_time, header, block_names, (variables, values, comments, blocks))
