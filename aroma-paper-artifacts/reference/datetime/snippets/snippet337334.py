import inspect
import operator
import re
from datetime import datetime
from decimal import Decimal
from enum import Enum
from functools import reduce
import pymongo
from bson import ObjectId
from pymongo.collection import Collection, ReturnDocument
from pymongo.errors import CollectionInvalid
from appkernel.configuration import config
from appkernel.util import OBJ_PREFIX
from .model import Model, Expression, AppKernelException, SortOrder, Property, Index, TextIndex, UniqueIndex, CustomProperty


@classmethod
def save_object(cls, model: Model, object_id=None):
    document = Model.to_dict(model, convert_id=True, converter_func=mongo_type_converter_to_dict)
    (has_id, doc_id, document) = MongoRepository.prepare_document(document, object_id)
    now = datetime.now()
    document.update(updated=now)
    if has_id:
        if ('version' in document):
            del document['version']
        if ('inserted' in document):
            del document['inserted']
        upsert_expression = {'$set': document, '$setOnInsert': {'inserted': now}, '$inc': {'version': 1}}
        update_result = cls.get_collection().update_one({'_id': doc_id}, upsert_expression, upsert=True)
        db_id = (update_result.upserted_id or doc_id)
    else:
        document.update(inserted=now, version=1)
        insert_result = cls.get_collection().insert_one(document)
        db_id = insert_result.inserted_id
    model.id = db_id
    return model.id
