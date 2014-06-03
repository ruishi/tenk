"""Unit tests for Skill class"""

from tenk import skills
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

    def test_calc_level(self):
        """skills should accurately calculate skill level"""
        skill = skills.Skill("programming", 0)
        self.assertEqual(0, skill.calc_level())
        skill.hours = 5
        self.assertEqual(0, skill.calc_level())
        # test boundary values
        skill.hours = 100
        self.assertEqual(1, skill.calc_level())
        skill.hours = 99
        self.assertEqual(0, skill.calc_level())
        skill.hours = 9999
        self.assertEqual(99, skill.calc_level())
        skill.hours = 10000
        self.assertEqual(100, skill.calc_level())
        # test 10K+ hours
        skill.hours = 20000
        self.assertEqual(100, skill.calc_level())

    def test_calc_progress(self):
        skill = skills.Skill("piano", 0)
        self.assertEqual(0, skill.calc_progress())
        skill.hours = 50
        self.assertEqual(50, skill.calc_progress())
        skill.hours = 86
        self.assertEqual(86, skill.calc_progress())
        skill.hours = 500
        self.assertEqual(0, skill.calc_progress())
        skill.hours = 586
        self.assertEqual(86, skill.calc_progress())
        skill.hours = 10000
        self.assertEqual(100, skill.calc_progress())
        skill.hours = 20000
        self.assertEqual(100, skill.calc_progress())

if __name__ == "__main__":
    unittest.main()
