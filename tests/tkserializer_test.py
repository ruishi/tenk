#!usr/bin/env python3
################################################################################
#author: RD Galang
#description: Tests custom JSON serializer
################################################################################

import os
import unittest
import tkserializer
from users import User
import json

class TKSerializerTest(unittest.TestCase):
    def test_serializer(self):
        """serializer should successfully convert from 
        custom classes to json and vice versa"""
        user = User("rdg")
        user.add_skill("programming", 50)
        user.add_skill("chinese", 200)
        with open('test.tk', encoding='utf-8', mode='w') as f:
            json.dump(user, f, default=tkserializer.to_json, indent=2)
        with open('test.tk', encoding='utf-8', mode='r') as f:
            user2 = json.load(f, object_hook=tkserializer.from_json)
        self.assertEqual(user, user2)
        

if __name__ == '__main__':
    unittest.main()
