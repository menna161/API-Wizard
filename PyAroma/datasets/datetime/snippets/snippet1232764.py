from pathlib import Path
from typing import Dict, Union
from .generators import parameter_sweep
from .phantomconfig import PhantomConfig


def read_dict(dictionary: Dict, dtype: str=None) -> PhantomConfig:
    'Initialize PhantomConfig from a dictionary.\n\n    Parameters\n    ----------\n    dictionary\n        A dictionary of the form:\n            {\'variable\': [value, comment, block], ...}\n        There are two special keys,\n            \'__header__\': a list of strings, corresponding to lines in\n                          the "header" of a Phantom config file,\n            \'__datetime__\': a datetime.datetime object for the time\n                            stamp of the file.\n    dtype\n        The dictionary type: either \'nested\' or \'flat\'. The default is\n        \'nested\'.\n\n    Returns\n    -------\n    PhantomConfig\n        Generated from the dictionary.\n    '
    if (dtype is None):
        dtype = 'nested'
    return PhantomConfig(dictionary=dictionary, dictionary_type=dtype)
