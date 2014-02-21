#!usr/bin/env python3
################################################################################
#author: RD Galang
#description: This contains some code from my program, which are hard to test
#             normally. So I'm isolating the parts I'd like to test here.
################################################################################

def progressbar(skill):
    """This is from users.py, where I create a "progress bar"  for each skill
    based on hours completed and current level. Here I'm testing just
    one skill that's being passed in and I've omitted the print statement as
    that's not important here."""
    progmarkers = ':' * int(skill.calcprogress()/2)
    spaces = ' ' * (50 - int(skill.calcprogress()/2))
    return progmarkers, spaces
