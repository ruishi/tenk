################################################################################
#author: RD Galang
#desc: unit tests for skills.py
#TODO: test Skill.calcprogress()
################################################################################
import sys
sys.path.append("..")

import skills
import unittest

class TestSkills(unittest.TestCase):

    def test_get(self):
        """skills should properly return value of called attributes"""
        skill = skills.Skill("test skill", 3)
        self.assertEqual("test skill", skill.name)
        self.assertEqual(3, skill.hours)

    def test_set(self):
        """skills should return new values when setting attributes to 
        other values"""
        skill = skills.Skill("test skill", 3)
        skill.name = "new skill"
        skill.hours = 1
        self.assertEqual("new skill", skill.name)
        self.assertEqual(1, skill.hours)

    def test_negative(self):
        """skills should not accept negative values for the hours attribute"""
        self.assertRaises(skills.OutOfRangeError, skills.Skill, 'x', -1)

    def test_calclevel(self):
        """skills should accurately calculate skill level"""
        skill = skills.Skill("programming", 0)
        self.assertEqual(0, skill.calclevel())
        skill.hours = 5
        self.assertEqual(0, skill.calclevel())
        skill.hours = 1000
        self.assertEqual(1, skill.calclevel())
        skill.hours = 9999
        self.assertEqual(9, skill.calclevel())
        skill.hours = 10000
        self.assertEqual(10, skill.calclevel())
        skill.hours = 20000
        self.assertEqual(10, skill.calclevel())

    def test_calcprogress(self):
        pass
if __name__ == "__main__":
    unittest.main()
