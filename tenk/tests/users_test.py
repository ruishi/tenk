############################################
#author: RD Galang
#desc: unit tests for users.py
#TODO: -add unit test for getskillnames()
###########################################
#import sys
#sys.path.append("..")

import tenk

import unittest

class TestUsers(unittest.TestCase):
 
    def test_add_skill(self):
        """users should be able to create skill object and add to skilset"""
        user = users.User("rachelg")
        user.add_skill("programming", 500)
        self.assertEqual("programming", user.skillset[0].name)
        self.assertEqual(500, user.skillset[0].hours)

    def test_remove(self):
        """users should properly remove specified value from skillset list"""
        user = users.User("rachelg", [])  #for some reason this won't work unless
                                          #you explicitly passed an empty list. otherwise
                                          #the skillset would start with len=1
                                          #however, testing in the interpreter did not have
                                          #this problem at all. and print statements in
                                          #testAddSkill showed proper list length for that
                                          #object.
        user.add_skill("piano", 3)
        user.add_skill("programming", 1000)
        user.add_skill("crochet", 200)
        user.add_skill("french", 2000)
        user.remove_skill("piano")
        self.assertEqual(3, len(user.skillset)) #checks if any skill was removed
        skillnames = [x.name for x in user.skillset]
        self.assertTrue("piano" not in skillnames) #checks if specified skill was removed

    def test_add_time(self):
        """users should be able to add time to any skill"""
        user = users.User("rachelg")
        user.add_skill("programming", 500)
        user.add_time("programming", 25)
        self.assertEqual(525, user.skillset[0].hours)

    def test_negative(self):
        user = users.User("rachelg")
        user.add_skill("x")
        """users should not accept negative values when adding time to skill"""
        self.assertRaises(users.OutOfRangeError, user.add_time, 'x', -1)


if __name__ == "__main__":
    unittest.main()
