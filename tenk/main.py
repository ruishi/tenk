################################################################################
# author: RD Galang
# filename: tenk.py
# description: Keeps track of time spent developing various
#              skills
################################################################################

import os
from sys import exit
from tenk.users import User
import tenk.tkserializer as tkserializer
import json
import glob

def main():
    """"Command-line menu interface entry point for tenk."""

    u_choice = menu('u')

    if u_choice == 'create':
        username = input("Desired username: ")
        user = User(username)
        print("\nWelome {}!\n".format(username))
        s_choice = menu('ms')
    elif u_choice == 'load':
        u_file = menu('l')
        check_storage()
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

    check_storage()
    u_file = os.path.join(os.path.expanduser('~'),
                          'tenk/{}.tk'.format(user.name))
    with open(u_file, encoding='utf-8', mode='w') as f:
        json.dump(user, f, indent=2, default=tkserializer.to_json)
        exit(0)

def check_storage():
    """Checks if there's a tenk folder in the user's home directory.
    Creates one if one doesn't exist."""
    if not os.path.exists(os.path.join(os.path.expanduser('~'), 'tenk')):
        os.makedirs(os.path.join(os.path.expanduser('~'), 'tenk'))

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
        user_list = glob.glob(os.path.expanduser('~/tenk/*.tk'))
        if not user_list:
            print("No user data found.")
            exit(1)
        elif len(user_list) == 1:
            return user_list[0]
        else:
            user_choice_dict = generate_dict(user_list)
            print("Please select an option:")
            for i in range(len(user_list)):
                print("{0}. {1}".format(i + 1, user_list[i][:-3]))

            return choose_from(user_choice_dict)

def choose_from(choice_dict):
    """Given a dictionary of menu choices, returns a choice."""
    choice = input()
    if choice in choice_dict:
        return choice_dict[choice]
    else:
        print("Not a valid option.")

def generate_dict(xs):
    """Creates a dictionary where the key is a string representing
    a number and the value is an element of xs"""
    return {str(i + 1):xs[i] for i in range(len(xs))}

if __name__ == '__main__':
    main()
