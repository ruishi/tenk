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

if __name__ == "__main__":
    unittest.main()
