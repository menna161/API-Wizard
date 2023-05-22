from unittest.mock import call
import pandas as pd
import pymongo
import pymongo.errors
import pytest
import pdmongo as pdm


def test_to_mongo_with_if_exists_replace_calls_drop(mocker):
    collection_name = 'ACollection'
    mock_db = mocker.patch('pymongo.database.Database')
    pdm.to_mongo(pd.DataFrame(), collection_name, mock_db, if_exists='replace')
    mock_db[collection_name].drop.assert_called_once()
