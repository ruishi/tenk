################################################################################
#author: RD Galang
#desc: class and methods for skills. 
#TODO: -create improved, sensical leveling system
################################################################################

class OutOfRangeError(ValueError): pass

class Skill:
    """Holds and calculates skill progress data.

    Attributes:
    name (str) -- name of the skill
    hours (float) -- number of hours spent practicing"""

    def __init__(self, name, hours = 0):
        self.name = name
        if hours >= 0:
            self.hours = hours
        else:
            raise OutOfRangeError("hours should be positive")

    def calclevel(self):
        """Calculates the "level" a user is at for the skill. 
        
        Keyword arguments: None

        Returns int"""

        level = 0
        levels = range(0,11) #levels 0-10
        for i in levels:
            max = (i + 1) * 1000
            level = i
            if self.hours < max:
                return level
        return level

    def calcprogress(self):
        """Calculates the progress being made in a certain skill. Progress
        is determined for the user's level in the skill, to improve
        morale and progress reports.

        Keyword arguments: None

        Returns: Float"""

        level = self.calclevel()
        levelmax = 1000 * (level + 1)
        return (self.hours/levelmax) * 100        

    """Comparison methods for testing"""
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
