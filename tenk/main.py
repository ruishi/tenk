"""CLI interface for tenk"""

import os
from sys import exit
import json
import glob
import argparse
import functools

from tenk.users import User
import tenk.tkserializer as tkserializer

no_data_msg = "You have no data!"

def get_data_path():
    """Returns path to user's data file if it exists. Otherwise returns
    None"""
    data_paths = glob.glob(os.path.join(os.path.expanduser('~'),
                                        'tenk/*.tk'))
    if data_paths:
        return data_paths[0]
    else:
        return None

def save(user):
    u_file = get_data_path()
    with open(u_file, encoding='utf-8', mode='w') as f:
        json.dump(user, f, indent=2, default=tkserializer.to_json)

def load_user(create=False):
    """Load a user's tk file into a User object. If create is True,
    then a user object will be created if no tk file exists."""
    if os.path.exists(os.path.join(os.path.expanduser('~'), 'tenk')):
        u_file = get_data_path()
        with open(u_file, encoding='utf-8', mode='r') as f:
            user = json.load(f, object_hook=tkserializer.from_json)
        return user
    else:
        os.makedirs(os.path.join(os.path.expanduser('~'), 'tenk'))
        if create:
            u_file = os.path.join(os.path.expanduser('~'),
                                  'tenk/default.tk')
            open(u_file, 'a').close()
            return User("Default")
        else:
            return None

def generate_dict(xs):
    """Creates a dictionary where the key is a string representing
    a number and the value is an element of xs"""
    return {float(i + 1):xs[i] for i in range(len(xs))}

def add_time(choice, time):
    user = load_user(create=False)
    if user:
        skill = generate_dict(user.get_skill_names())[choice]
        user.add_time(skill, time)
        save(user)
    else:
        print(no_data_msg)

def add_skill(name, hours=0):
    user = load_user(create=True)
    user.add_skill(name, hours)
    save(user)

def remove_skill(choice):
    user = load_user(create=False)
    if user:
        skill = generate_dict(user.get_skill_names())[choice]
        user.remove_skill(skill)
        save(user)
    else:
        print(no_data_msg)

def list_skills():
    user = load_user()
    if user:
        for idx, skill in enumerate(user.get_skill_names()):
            print("{}. {}".format(idx + 1, skill))
    else:
        print(no_data_msg)

def print_progress():
    """Print a user's progress"""
    user = load_user()
    if user:
        user.print_progress()
    else:
        print(no_data_msg)

if __name__ == '__main__':
    parser  = argparse.ArgumentParser(prog="python3 -m tenk.main")
    parser.add_argument('-l', '--ls',
                        action='store_true',
                        help="List skillset")
    parser.add_argument('-s', '--skill',
                        nargs='+',
                        metavar=('name', 'hours'),
                        help="Add skill to skillset")
    parser.add_argument('-t', '--time',
                        nargs=2,
                        type=float,
                        metavar=('skill', 'time'),
                        help=("Add time to a skill"))
    parser.add_argument('-d', '--delete',
                        type=float,
                        metavar='skill',
                        help="Delete a skill")
    parser.add_argument('-p', '--progress',
                        action='store_true',
                        help="Print progress")
    args = parser.parse_args()

    if args.ls:
        list_skills()
    elif args.progress:
        print_progress()
    elif args.time:
        add_time(args.time[0], float(args.time[1]))
    elif args.skill:
        if len(args.skill) == 2:
            add_skill(args.skill[0], args.skill[1])
        else:
            add_skill(args.skill[0])
    elif args.delete:
        remove_skill(args.delete)
    else:
        parser.print_help()
