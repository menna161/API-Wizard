import datetime
import logging
from samples import resource
from utils import emit
from azure.devops.v5_1.work_item_tracking.models import Wiql


@resource('work_items')
def get_work_items_as_of(context):
    wit_client = context.connection.clients.get_work_item_tracking_client()
    desired_ids = range(1, 51)
    as_of_date = (datetime.datetime.now() + datetime.timedelta(days=(- 7)))
    work_items = wit_client.get_work_items(ids=desired_ids, as_of=as_of_date, error_policy='omit')
    for (id_, work_item) in zip(desired_ids, work_items):
        if work_item:
            print_work_item(work_item)
        else:
            emit('(work item {0} omitted by server)'.format(id_))
    return work_items
