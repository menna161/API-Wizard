import json
import os
import uuid
from datetime import datetime
from numbers import Number
import requests
from django.conf import settings
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from pyplan.pyplan.common.baseService import BaseService
from pyplan.pyplan.common.utils import _zipFiles
from pyplan.pyplan.dashboard.models import Dashboard
from pyplan.pyplan.dashboardstyle.models import DashboardStyle
from pyplan.pyplan.department.models import Department
from pyplan.pyplan.usercompanies.models import UserCompany
from .models import Report
from .serializers import ExportItemsSerializer


def exportItemsAndPublish(self, data):
    response = None
    reports = Report.objects.filter(pk__in=data['report_ids'])
    dashboards = Dashboard.objects.filter(pk__in=data['dashboard_ids'])
    styles = []
    styles.extend(DashboardStyle.objects.filter(dashboards__id__in=data['dashboard_ids']).all())
    self._getStyles(reports, styles)
    to_save = {'dashboards': dashboards, 'reports': reports, 'styles': list(set(styles))}
    to_save_serialized = json.dumps(ExportItemsSerializer(to_save).data, indent=None)
    storage = FileSystemStorage(os.path.join(settings.MEDIA_ROOT, 'models'))
    file_path = os.path.join(storage.base_location, os.path.normpath(data['model_folder']), 'itemsToPublish.json')
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, 'w') as json_file:
        json_file.write(to_save_serialized)
    zip_file = None
    zip_file = _zipFiles([os.path.normpath(data['model_folder'])], storage.base_location, os.path.join(storage.base_location, f"{os.path.normpath(data['model_folder'])}.zip"), True, None)
    if zip_file:
        files = {'files': open(zip_file, 'rb')}
        values = {'username': data['username'], 'uuid': data['uuid'], 'model_id': data['model_id'], 'zip_name': zip_file[zip_file.rfind(os.path.sep):], 'model_name': self.client_session.modelInfo.uri[(self.client_session.modelInfo.uri.rfind(os.path.sep) + 1):]}
        req = requests.put('https://api.pyplan.com/api/reportManager/publishItems/', files=files, data=values)
        response = req.text
    storage.delete(zip_file)
    storage.delete(file_path)
    return response
