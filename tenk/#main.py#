##############################################################
# author: RD Galang
# filename: tenk.py
# description: Keeps track of time spent developing various 
#              skills
# note: This is my first program using Python 3. There will
#       be a lot of comments that make this obvious.
# TODO: -Switch to json
#       -GUI wrapper
#############################################################

'''
try:
  import someMod
except ImportError:
  someMod = None

then can check for presence using if -
if chardet:
  #do something
else:
  #continue anyway

clearly, the above is best for 3rd party libraries

when two modules implement API, can import one, but fall back to a
different one if the first fails:

try:
  from lxml import etree
except ImportError:
  import xml.etree.ElementTree as etree

notice the fallback is renamed as etree so code body does not need to be
more complicated with if statements

'''

import os #module to retrieve information on and manipulate files, directories, etc.
from sys import exit
from users import * #if you use from __ import __ rather than import __, you can reference a method without naming the class.
                    #ex: instantiating with User(username) instead of users.Username(username)
import pickle

'''
error types:
ImportError
NameError - call variable that DNE
ValueError - value not in list
'''

def main():
    """"Command-line interface for tenk.

    Keyword arguments: None

    Returns None"""


    u_choice = menu('u')
    user = User("placeholder")
    
    if u_choice == 'create':
        username = input("Desired username: ")
        user.name = username
        s_choice = menu('s')
    elif u_choice == 'load':
        username = input("Username: ")
        u_file = "{}.pickle".format(username)
        with open(u_file, 'rb') as f:
            user = pickle.load(f)
        s_choice = menu('ms')
    else:
        exit(0)

    while s_choice != "exit":
        if s_choice == 'add_skill':
            skill = input("Skill name: ")
            try:
                hours = float(input("Initial times (hours): "))
                user.add_skill(skill, hours)
            except ValueError:
                print("a valid number must be entered")
                exit(1)
        elif s_choice == 'delete':
            skill = menu('s', user)
            user.remove_skill(skill)
        elif s_choice == 'add_time':
            skill = menu('s', user)
            try:
                hours = float(input("Number of hours to add: "))
                user.add_time(skill, hours)
            except ValueError:
                print("a valid number must be entered")
                exit(1)
        elif s_choice == 'print':
            user.printprogress()
            print()

        s_choice = menu('ms')

    u_file = "{}.pickle".format(user.name)
    with open(u_file, 'wb') as f:
        pickle.dump(user, f)
        exit(0)
    

def menu(key, user=None):
    """Creates requested menu and returns user's choice.

    Keyword arguments:
    key -- menu identifier

    Returns str or None."""
    
    user_menu_dict = {'1': 'create', '2': 'load', '3': 'exit'}
    skill_menu_dict = {'1': 'add_skill', '2':'delete', '3':'add_time', '4':'print', '5':'exit'}

    if key == 'u': #user menu
        print("Please select an option:")
        print("1. Create user")
        print("2. Load user")
        print("3. Exit")
        
        choice = input("")
        if choice in user_menu_dict:
            return user_menu_dict[choice]
        else:
            print("Not a valid option.")

    elif key == 'ms': #modify skill menu
        print("1. Add skill")
        print("2. Delete skill")
        print("3. Add time")
        print("4. Print progress")
        print("5. Exit")

        choice = input("")
        if choice in skill_menu_dict:
            return skill_menu_dict[choice]
        else:
            print("Not a valid option.")
    elif key == 's': #skill menu
       skill_names = user.getskillnames()
       skill_choices_dict = {str(i + 1):skill_names[i] for i in range(len(skill_names))}
       print("Please select an option:")
       for i in range(len(skill_names)):
           print("{0}. {1}".format(i + 1, skill_names[i]))

       choice = input()
       if choice in skill_choices_dict:
           return skill_choices_dict[choice]
       else:
           print("Not a valid option.")

#This is used to test a module.
#All modules are objects (like everything else in python) with a
#built-in attribute __name__, which changes depending on how the
#module is being used. If you import it, __name__ is the module's
#filename. Otherwise __name__ is __main__.
if __name__ == '__main__':
    main()
