import unittest
from random import randint
from ands.ds.Stack import Stack


def test_push_many(self):
    s = Stack()
    for i in range(randint(2, 100)):
        s.push(i)
        self.assertEqual(s.size, (i + 1))
        self.assertFalse(s.is_empty())
        self.assertEqual(s.top(), i)
