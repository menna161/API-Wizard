import pytest
from pupa.scrape.schemas.person import schema
from pupa.scrape.base import BaseModel, SourceMixin, ContactDetailMixin, LinkMixin, AssociatedLinkMixin, OtherNameMixin, IdentifierMixin


def test_setattr():
    m = GenericModel()
    with pytest.raises(ValueError):
        m.some_random_key = 3
    m._id = 'new id'
