####################################
#author: RD Galang
#desc: class and methods for users
#TODO: ...
####################################

import skills

class OutOfRangeError(ValueError): pass

class User():

    def __init__(self, username, skillset = []):
        self.name = username
        self.skillset = skillset

    def add_skill(self, skillname, hours = 0):
        """Adds a skill to a user's skillset.

        Keyword arguments:
        skillname -- the name of the skill being added
        hours -- the amount of time spent developing the skill so far

        Returns None. """

        skill = skills.Skill(skillname, hours)
        self.skillset.append(skill)

    def remove_skill(self, skillname):
        """Removes a skill from a user's skillset.

        Keyword arguments:
        skillname -- the name of the skill being removed

        Returns None."""

        for skill in self.skillset:
            if skillname == skill.name:
                self.skillset.remove(skill)

    def add_time(self, skillname, time):
        """Add to time spent developing a skill.

        Keyword arguments:
        skillname - the name of the skill to add hours to

        Returns None."""
        
        skill_exists = False

        if time < 0:
            raise OutOfRangeError("time added must be positive")

        for index, skill in enumerate(self.skillset):
            if skillname == skill.name:
                self.skillset[index].hours += time
                skill_exists = True

        if not skill_exists:
            print("skill does not exist.")


    def getskillnames(self):
        skill_names = [skill.name for skill in self.skillset]
        return skill_names

    def printprogress(self):
        for skill in self.skillset:
            p = ':' * int(skill.calcprogress()/2)
            s = ' ' * (50 - int(skill.calcprogress()/2))
            print("{0} ({1}):\n [{2}{3}]".format(skill.name, skill.hours, p, s))
