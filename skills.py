################################################################################
#author: RD Galang
#desc: class and methods for skills. 
#TODO: -Implement levels
################################################################################

class OutOfRangeError(ValueError): pass

class Skill():

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
        levels = range(1,11) #levels 1-10
        for i in levels:
            max = i * 1000
            if self.hours < max:
                level = i
                break
        return level

    def calcprogress(self):
        """Calculates the progress being made in a certain skill. Progress
        is determined for the user's level in the skill, to improve
        morale and progress reports.

        Keyword arguments: None

        Returns: Float"""

        level = self.calclevel()
        levelmax = 1000 * level
        return (self.hours/levelmax) * 100        
