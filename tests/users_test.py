"""Unit tests for User class"""
#TODO: add unit test to ensure duplicate skills are not added

import tenk.users as users

import unittest

class TestUsers(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.user = users.User("rdg")

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.user.skillset[:]

    def test_add_skill(self):
        """users should be able to create skill object and add to skillset"""
        self.user.add_skill('programming', 500)
        self.assertEqual('programming', self.user.skillset[0].name)
        self.assertEqual(500, self.user.skillset[0].hours)

    def test_remove(self):
        """users should properly remove specified value from skillset list"""
        self.user.add_skill('programming', 500)
        self.user.add_skill('piano', 3)
        self.user.add_skill('french', 2000)
        self.user.add_skill('p', 5)
        self.user.remove_skill('p')
        #ensure only one skill is removed
        self.assertEqual(3, len(self.user.skillset))
        skillnames = [x.name for x in self.user.skillset]
        #ensures specified skill was removed
        self.assertTrue("p" not in skillnames)

    def test_getskillnames(self):
        """users should successfully retrieve all skill names in a
        user's skillset"""
        self.user.add_skill('programming', 500)
        self.user.add_skill('piano', 5)
        self.user.add_skill('french', 100)
        self.assertEqual(['programming', 'piano', 'french'],
                         self.user.getskillnames())

    def test_add_time(self):
        """users should be able to add time to any skill"""
        self.user.add_skill('programming', 500)
        self.user.add_time('programming', 25)
        self.assertEqual(525, self.user.skillset[0].hours)

    def test_add_time2(self):
        """users should not be able to add time to a non-existent skill"""
        self.assertRaises(users.DoesNotExistError,
                          self.user.add_time, 'spellunking', 25)

    def test_negative(self):
        """users should not accept negative values when adding time to skill"""
        self.user.add_skill('programming', 100)
        self.assertRaises(users.OutOfRangeError,
                          self.user.add_time, 'programming', -1)

if __name__ == "__main__":
    unittest.main()
