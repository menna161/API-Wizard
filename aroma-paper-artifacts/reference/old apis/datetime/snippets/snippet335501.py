from datetime import datetime, timezone, timedelta
import pytest
from appdaemon.plugins.hass.hassapi import Hass
from pytest import raises
from appdaemontestframework import automation_fixture
from appdaemontestframework.given_that import StateNotSetError


def test_last_updated_changed__get_all__return_iso_formatted_date(given_that, automation: MockAutomation):
    utc_plus_3 = timezone(timedelta(hours=3))
    updated = datetime(year=2020, month=3, day=3, hour=11, minute=27, second=37, microsecond=3, tzinfo=utc_plus_3)
    changed = datetime(year=2020, month=3, day=14, hour=20, microsecond=123456, tzinfo=timezone.utc)
    given_that.state_of(LIGHT).is_set_to('on', attributes={'brightness': 11, 'color': 'blue'}, last_updated=updated, last_changed=changed)
    expected_updated = '2020-03-03T11:27:37.000003+03:00'
    expected_changed = '2020-03-14T20:00:00.123456+00:00'
    all_attributes = automation.get_all_attributes_from_light()
    assert (all_attributes['last_updated'] == expected_updated)
    assert (all_attributes['last_changed'] == expected_changed)
    assert (all_attributes == {'state': 'on', 'last_updated': expected_updated, 'last_changed': expected_changed, 'entity_id': LIGHT, 'attributes': {'brightness': 11, 'color': 'blue'}})
