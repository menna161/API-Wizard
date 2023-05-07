import pytest
import argparse
from datetime import datetime, timezone, timedelta
from freezegun import freeze_time
from opencivicdata.core.models import Person, Organization, Jurisdiction, Division
from pupa.cli.commands.clean import Command


@pytest.mark.django_db
def test_remove_stale_objects(subparsers):
    _ = create_jurisdiction()
    o = Organization.objects.create(name='WWE', jurisdiction_id='jid')
    p = Person.objects.create(name='George Washington', family_name='Washington')
    m = p.memberships.create(organization=o)
    expected_stale_objects = {p, o, m}
    a_week_from_now = (datetime.now(tz=timezone.utc) + timedelta(days=7))
    with freeze_time(a_week_from_now):
        p = Person.objects.create(name='Thomas Jefferson', family_name='Jefferson')
        p.memberships.create(organization=o)
        Command(subparsers).remove_stale_objects(7)
        for obj in expected_stale_objects:
            was_deleted = (not type(obj).objects.filter(id=obj.id).exists())
            assert was_deleted
