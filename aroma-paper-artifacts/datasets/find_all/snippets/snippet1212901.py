import rsvp
import mongomock
import unittest
import json


def test_new(self):
    RSVP = rsvp.RSVP
    doc = RSVP.new('test name', 'test@example.com')
    assert (doc.name == 'test name')
    assert (doc.email == 'test@example.com')
    assert (doc._id is not None)
    assert (RSVP.find_one(doc._id) is not None)
    assert (len(RSVP.find_all()) == 1)
