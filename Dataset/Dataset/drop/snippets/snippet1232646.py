from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union
import pymongo.errors
from pandas import DataFrame
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.results import InsertManyResult
from pymongo.uri_parser import parse_uri


def _handle_exists_collection(name: str, exists: Optional[str], db: Database) -> None:
    "\n    Handles the `if_exists` argument of `to_mongo`.\n\n    Parameters\n    ----------\n    if_exists: str\n        Can be one of 'fail', 'replace', 'append'\n            - fail: A ValueError is raised\n            - replace: Collection is deleted before inserting new documents\n            - append: Documents are appended to existing collection\n    "
    if (exists == 'fail'):
        if _collection_exists(db, name):
            raise ValueError(f"Collection '{name}' already exists.")
        return
    if (exists == 'replace'):
        if _collection_exists(db, name):
            db[name].drop()
        return
    if (exists == 'append'):
        return
    raise ValueError(f"'{exists}' is not valid for if_exists")
