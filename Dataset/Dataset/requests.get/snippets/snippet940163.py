import json
import os
import requests
import wx
from .design_frame import MyDialogUpdateLocation
from ..structs_classes.location_group import LocationList


def work():
    try:
        r = requests.get(self.available_list[index], timeout=1000)
        if (r.status_code == 200):
            self.load_data = json.loads(r.text)
        self.compare()
        self.m_staticText_info.SetLabel(f'加载完成！来自{event.GetString()}提供的本地化方案')
    except Exception as info:
        wx.MessageBox(f'{info.__str__()}')
