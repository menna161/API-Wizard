import warnings
from typing import Any, Dict, Optional, Tuple
from django import forms
from django.forms.widgets import DateTimeBaseInput
from ._config import WidgetConfig
from .schemas import InputAttrs, WidgetOptions, WidgetVariant
from .settings import get_widget_settings


@property
def media(self) -> forms.Media:
    'Generate widget Media.'
    settings = get_widget_settings()
    return forms.Media(css={'all': tuple_exclude_none(settings.bootstrap_icon_css_url, settings.datetimepicker_css_url, (settings.app_static_url + 'css/datepicker-widget.css'))}, js=tuple_exclude_none(settings.momentjs_url, settings.datetimepicker_js_url, (settings.app_static_url + 'js/datepicker-widget.js')))
