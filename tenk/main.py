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

import os
from sys import exit
from users import User
import tkserializer
import json
import glob

def main():
    """"Command-line interface for tenk.

    Keyword arguments: None

    Returns None"""

    #user = User("")
    u_choice = menu('u')
    
    if u_choice == 'create':
        username = input("Desired username: ")
        user = User(username)
        print("\nWelome {}!\n".format(username))
        s_choice = menu('ms')
    elif u_choice == 'load':
        u_file = menu('l')
        with open(u_file, encoding='utf-8', mode='r') as f:
            user = json.load(f, object_hook=tkserializer.from_json)
        print("\nWelcome back {}!\n".format(user.name))
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
    
    u_file = "{}.tk".format(user.name)
    with open(u_file, encoding='utf-8', mode='w') as f:
        json.dump(user, f, indent=2, default=tkserializer.to_json)
        exit(0)
    

def menu(key, user=None):
    """Creates requested menu and returns user's choice.

    Keyword arguments:
    key -- menu identifier

    Returns str or None."""
    
    user_menu_dict = {'1': 'create', '2': 'load', '3': 'exit'}
    skill_menu_dict = {'1': 'add_skill', '2':'delete', '3':'add_time', 
                       '4':'print', '5':'exit'}

    if key == 'u': #user menu
        print("Please select an option:")
        print("1. Create user")
        print("2. Load user")
        print("3. Exit")
        
        return choose_from(user_menu_dict)
    elif key == 'ms': #modify skill menu
        print("1. Add skill")
        print("2. Delete skill")
        print("3. Add time")
        print("4. Print progress")
        print("5. Exit")

        return choose_from(skill_menu_dict)
    elif key == 's': #skill menu
        skill_names = user.getskillnames()
        skill_choices_dict = generate_dict(skill_names)
        print("Please select an option:")
        for i in range(len(skill_names)):
            print("{0}. {1}".format(i + 1, skill_names[i]))
        return choose_from(skill_choices_dict)
    elif key == 'l': #load user menu
        user_list = glob.glob("*.tk")
        if len(user_list) == 1:
            return user_list[0]
        else:
            user_choice_dict = generate_dict(user_list)
            print("Please select an option:")
            for i in range(len(user_list)):
                print("{0}. {1}".format(i + 1, user_list[i][:-3]))

            return choose_from(user_choice_dict)

def choose_from(choice_dict):
    choice = input()
    if choice in choice_dict:
        return choice_dict[choice]
    else:
        print("Not a valid option")

def generate_dict(xs):
    return {str(i + 1):xs[i] for i in range(len(xs))}

#This is used to test a module or run it as a script.
#All modules are objects (like everything else in python) with a
#built-in attribute __name__, which changes depending on how the
#module is being used. If you import it, __name__ is the module's
#filename. Otherwise __name__ is __main__.
if __name__ == '__main__':
    main()
