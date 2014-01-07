############################################
#author: Rachel Galang
#desc: class and methods for skills
#TODO: -Implement levels
###########################################

class OutOfRangeError(ValueError): pass

class Skill():

    def __init__(self, name, hours = 0):
        self.name = name
        if hours >= 0:
            self.hours = hours
        else:
            raise OutOfRangeError("hours should be positive")

    def calcprogress(self):
        return (self.hours/10000) * 100
