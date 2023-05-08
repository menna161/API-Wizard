import json
import logging
import os
import datetime
from amti import settings


def expire_batch(client, batch_dir):
    "Expire all the (unanswered) HITs in the batch.\n\n    Parameters\n    ----------\n    client : MTurk.Client\n        a boto3 client for MTurk.\n    batch_dir : str\n        the path to the directory for the batch.\n\n    Returns\n    -------\n    Dict[str, int]\n        A dictionary mapping strings to integers. The dictionary will\n        have the following form::\n\n            {\n                'batch_id': batch_id,\n            }\n\n        where ``batch_id`` is the UUID for the batch.\n    "
    (batch_dir_name, batch_dir_subpaths) = settings.BATCH_DIR_STRUCTURE
    (batchid_file_name, _) = batch_dir_subpaths['batchid']
    incomplete_file_name = settings.INCOMPLETE_FILE_NAME
    batchid_file_path = os.path.join(batch_dir, batchid_file_name)
    incomplete_file_path = os.path.join(batch_dir, settings.INCOMPLETE_FILE_NAME)
    with open(batchid_file_path) as batchid_file:
        batch_id = batchid_file.read().strip()
    if (not os.path.isfile(incomplete_file_path)):
        raise ValueError(f'No {incomplete_file_name} file was found in {batch_dir}. Please make sure that the directory is a batch that has open HITs to be expired.')
    with open(incomplete_file_path) as incomplete_file:
        hit_ids = json.load(incomplete_file)['hit_ids']
    logger.info(f'Expiring HITs in batch {batch_id}.')
    for hit_id in hit_ids:
        hit = client.update_expiration_for_hit(HITId=hit_id, ExpireAt=datetime.datetime.now())
    logger.info(f'All HITs in batch {batch_id} are now expired.')
    return {'batch_id': batch_id}
