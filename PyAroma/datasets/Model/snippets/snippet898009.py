import pytest
from pupa.scrape.schemas.person import schema
from pupa.scrape.base import BaseModel, SourceMixin, ContactDetailMixin, LinkMixin, AssociatedLinkMixin, OtherNameMixin, IdentifierMixin


def test_init_id():
    m = GenericModel()
    assert (len(m._id) == 36)
