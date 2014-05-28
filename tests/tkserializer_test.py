"""Tests custom JSON serializer"""


import os
import unittest
import tenk.tkserializer as tkserializer
from tenk.users import User
import json

class TKSerializerTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.user = User("rdg")

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.user.skillset[:]

    def test_serializer(self):
        """serializer should successfully convert from
        custom classes to json and vice versa"""
        self.user.add_skill("programming", 50)
        self.user.add_skill("chinese", 200)
        with open('test.tk', encoding='utf-8', mode='w') as f:
            json.dump(self.user, f, default=tkserializer.to_json, indent=2)
        with open('test.tk', encoding='utf-8', mode='r') as f:
            user2 = json.load(f, object_hook=tkserializer.from_json)
        os.remove('test.tk')
        self.assertEqual(self.user, user2)


if __name__ == '__main__':
    unittest.main()
