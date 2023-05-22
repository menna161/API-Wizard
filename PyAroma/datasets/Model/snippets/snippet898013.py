import pytest
from pupa.scrape.schemas.person import schema
from pupa.scrape.base import BaseModel, SourceMixin, ContactDetailMixin, LinkMixin, AssociatedLinkMixin, OtherNameMixin, IdentifierMixin


def test_add_contact_detail():
    m = GenericModel()
    m.add_contact_detail(type='fax', value='111-222-3333', note='office')
    assert (m.contact_details == [{'type': 'fax', 'value': '111-222-3333', 'note': 'office'}])
