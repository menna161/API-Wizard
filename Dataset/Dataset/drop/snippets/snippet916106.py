from typing import Dict, List, Tuple, Union
import numpy as np
import pandas as pd
from gym import Env
from gym import spaces


@staticmethod
def _get_user_data(user: pd.DataFrame) -> Dict[(int, Dict[(str, Union[(int, str)])])]:
    '\n        Create dictionary of user stats (e.g., age, occupation, gender)\n        to use as inputs into other functions.\n        '
    tmp_user = user.drop(['zip_code'], axis=1)
    tmp_user.index = tmp_user.user_id
    tmp_user = tmp_user.drop(['user_id'], axis=1)
    return tmp_user.to_dict(orient='index')
