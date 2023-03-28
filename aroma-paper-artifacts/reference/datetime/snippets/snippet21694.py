from django.http import JsonResponse
from django.http import HttpResponse
from data.models import SeenByHour
from data.queries import prepare_df_datetime_index
from data.queries import compute_kpis


def aggregations_by_box_id(request, box_id=None):
    "\n    FOR D3\n    Returns a list of dictionaries containing the following\n    [{'time': '<tz-naive timestamp>', 'seen': 115},{...}]\n    "
    seen_filter = SeenByHour.pdobjects
    if (box_id is not None):
        seen_filter = seen_filter.filter(box_id=box_id)
    seen_by_hour_df = prepare_df_datetime_index(seen_filter.to_dataframe(fieldnames=['hour_start', 'seen', 'seen_also_in_preceding_hour']), time_column='hour_start')
    seen_by_hour_df = seen_by_hour_df.reset_index()
    seen_by_hour_df['time'] = seen_by_hour_df['time'].map((lambda x: x.replace(tzinfo=None).timestamp()))
    data = seen_by_hour_df.to_dict('records')
    return JsonResponse(data, safe=False)
