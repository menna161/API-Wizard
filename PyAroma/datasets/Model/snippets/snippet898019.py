import pytest
from pupa.scrape.schemas.person import schema
from pupa.scrape.base import BaseModel, SourceMixin, ContactDetailMixin, LinkMixin, AssociatedLinkMixin, OtherNameMixin, IdentifierMixin


def test_add_name():
    m = GenericModel()
    m.add_name('Thiston', note='What my friends call me')
    assert (m.other_names == [{'name': 'Thiston', 'note': 'What my friends call me'}])
    m.add_name('Johnseph Q. Publico', note='Birth name', start_date='1920-01', end_date='1949-12-31')
    assert (m.other_names == [{'name': 'Thiston', 'note': 'What my friends call me'}, {'name': 'Johnseph Q. Publico', 'note': 'Birth name', 'start_date': '1920-01', 'end_date': '1949-12-31'}])
