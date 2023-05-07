import pytest
from pupa.scrape.schemas.person import schema
from pupa.scrape.base import BaseModel, SourceMixin, ContactDetailMixin, LinkMixin, AssociatedLinkMixin, OtherNameMixin, IdentifierMixin


def test_add_associated_link_on_duplicate_ignore():
    m = GenericModel()
    m._add_associated_link('_associated', 'something', 'http://example.com', text='', media_type='text/html', on_duplicate='ignore')
    m._add_associated_link('_associated', 'something else', 'http://example.com', text='', media_type='text/html', on_duplicate='ignore')
    assert (len(m._associated) == 1)
    assert (len(m._associated[0]['links']) == 1)
    assert (m._associated[0]['note'] == 'something')
