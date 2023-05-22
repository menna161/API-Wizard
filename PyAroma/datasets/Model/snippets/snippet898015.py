import pytest
from pupa.scrape.schemas.person import schema
from pupa.scrape.base import BaseModel, SourceMixin, ContactDetailMixin, LinkMixin, AssociatedLinkMixin, OtherNameMixin, IdentifierMixin


def test_add_associated_link_match():
    m = GenericModel()
    m._add_associated_link('_associated', 'something', 'http://example.com/1.txt', text='', media_type='text/plain', on_duplicate='error')
    m._add_associated_link('_associated', 'something', 'http://example.com/1.pdf', text='', media_type='application/pdf', on_duplicate='error')
    assert (len(m._associated) == 1)
    assert (len(m._associated[0]['links']) == 2)
