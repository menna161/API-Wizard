import pytest
from pupa.scrape.schemas.person import schema
from pupa.scrape.base import BaseModel, SourceMixin, ContactDetailMixin, LinkMixin, AssociatedLinkMixin, OtherNameMixin, IdentifierMixin


def test_add_source():
    m = GenericModel()
    m.add_source('http://example.com/1')
    m.add_source('http://example.com/2', note='xyz')
    assert (m.sources == [{'url': 'http://example.com/1', 'note': ''}, {'url': 'http://example.com/2', 'note': 'xyz'}])
