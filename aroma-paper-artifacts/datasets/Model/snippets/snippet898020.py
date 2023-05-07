import pytest
from pupa.scrape.schemas.person import schema
from pupa.scrape.base import BaseModel, SourceMixin, ContactDetailMixin, LinkMixin, AssociatedLinkMixin, OtherNameMixin, IdentifierMixin


def test_add_identifier():
    g = GenericModel()
    with pytest.raises(TypeError):
        g.add_identifier('id10t', foo='bar')
    g.add_identifier('id10t')
    g.add_identifier('l0l', scheme='kruft')
    assert (g.identifiers[(- 1)]['scheme'] == 'kruft')
    assert (g.identifiers[0]['identifier'] == 'id10t')
