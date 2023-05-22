import pytest
from pupa.scrape import Post as ScrapePost
from pupa.importers import PostImporter, OrganizationImporter
from opencivicdata.core.models import Organization, Post, Division, Jurisdiction
import datetime


@pytest.mark.django_db
def test_full_post():
    create_jurisdictions()
    org = Organization.objects.create(name='United States Executive Branch', classification='executive', jurisdiction_id='us')
    post = ScrapePost(label='executive', role='President', organization_id='~{"classification": "executive"}', start_date=datetime.date(2015, 5, 18), end_date='2015-05-19', maximum_memberships=2)
    post.add_contact_detail(type='phone', value='555-555-1234', note='this is fake')
    post.add_link('http://example.com/link')
    oi = OrganizationImporter('us')
    PostImporter('jurisdiction-id', oi).import_data([post.as_dict()])
    print(post.as_dict())
    p = Post.objects.get()
    assert ('ocd-post' in p.id)
    assert (p.label == post.label)
    assert (p.role == post.role)
    assert (p.organization_id == org.id)
    assert (p.maximum_memberships == 2)
    assert (p.contact_details.all()[0].type == 'phone')
    assert (p.contact_details.all()[0].value == '555-555-1234')
    assert (p.contact_details.all()[0].note == 'this is fake')
    assert (p.links.all()[0].url == 'http://example.com/link')
    assert (p.start_date == '2015-05-18')
    assert (p.end_date == '2015-05-19')
