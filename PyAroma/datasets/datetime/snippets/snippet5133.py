from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Post
from config import Config


def test_follow_posts(self):
    u1 = User(username='john', email='john@example.com')
    u2 = User(username='susan', email='susan@example.com')
    u3 = User(username='mary', email='mary@example.com')
    u4 = User(username='david', email='david@example.com')
    db.session.add_all([u1, u2, u3, u4])
    now = datetime.utcnow()
    p1 = Post(body='post from john', author=u1, timestamp=(now + timedelta(seconds=1)))
    p2 = Post(body='post from susan', author=u2, timestamp=(now + timedelta(seconds=4)))
    p3 = Post(body='post from mary', author=u3, timestamp=(now + timedelta(seconds=3)))
    p4 = Post(body='post from david', author=u4, timestamp=(now + timedelta(seconds=2)))
    db.session.add_all([p1, p2, p3, p4])
    db.session.commit()
    u1.follow(u2)
    u1.follow(u4)
    u2.follow(u3)
    u3.follow(u4)
    db.session.commit()
    f1 = u1.followed_posts().all()
    f2 = u2.followed_posts().all()
    f3 = u3.followed_posts().all()
    f4 = u4.followed_posts().all()
    self.assertEqual(f1, [p2, p4, p1])
    self.assertEqual(f2, [p2, p3])
    self.assertEqual(f3, [p3, p4])
    self.assertEqual(f4, [p4])
