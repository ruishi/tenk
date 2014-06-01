"""Manages hours and level for a skill."""

class OutOfRangeError(ValueError): pass

class Skill():

    def __init__(self, name, hours = 0):
        self.name = name
        if hours >= 0:
            self.hours = hours
        else:
            raise OutOfRangeError("hours should be positive")

    def calc_level(self):
        """Calculates the "level" a user is at for the skill. There are 100
        levels.

        Returns an int.
        """

        level = 0
        levels = range(0,101) # levels 0-100
        level_hours = 100 # the number of hours it takes to complete a level
        for i in levels:
            max_hours = (i + 1) * level_hours
            level = i
            if self.hours < max_hours:
                return level
        # if this part executes, then that means the user has exceeded
        # 10K hours and is already at level 100. So just return level,
        # which is set to 100 at this point.
        return level

    def calc_progress(self):
        """Calculates the progress being made in a certain skill. Progress
        is determined for the user's current level in the skill, to improve
        morale and progress reports.

        Keyword arguments: None

        Returns: Float"""
        if self.hours >= 10000:
            return 100
        level = self.calc_level()
        level_hours = 100
        return self.hours - (level_hours * level)

    def print_progress(self):
        """Prints a string representation of current progress"""
        progress = self.calc_progress()
        progmarkers = ':' * int(progress/2)
        spaces = ' ' * (50 - int(progress/2))
        print("{0} ({1}, level {2}):\n [{3}{4}]".format(self.name,
                                                        self.hours,
                                                        self.calc_level(),
                                                        progmarkers,
                                                        spaces))

    # Comparison methods for testing
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
