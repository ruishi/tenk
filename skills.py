############################################
#author: Rachel Galang
#desc: class and methods for skills
#TODO: -Write method to calculate progress
#       percentage for a given skill.
###########################################

class OutOfRangeError(ValueError): pass

class Skill():

    def __init__(self, name, hours = 0):
        self.name = name
        if hours >= 0:
            self.hours = hours
        else:
            raise OutOfRangeError("hours should be positive")
