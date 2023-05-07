import datetime
import pytest
from pupa.scrape import Person, Organization, Membership, Post
from pupa.utils import get_pseudo_id
from pupa.exceptions import ScrapeValueError


def test_person_add_membership_org():
    p = Person('Bob B. Bear')
    p.add_source('http://example.com')
    o = Organization('test org', classification='unknown')
    p.add_membership(o, role='member', start_date='2007', end_date=datetime.date(2015, 5, 8))
    assert (len(p._related) == 1)
    p._related[0].validate()
    assert (p._related[0].person_id == p._id)
    assert (p._related[0].organization_id == o._id)
    assert (p._related[0].start_date == '2007')
    assert (p._related[0].end_date == datetime.date(2015, 5, 8))
