"""CLI interface for tenk"""

import os
from sys import exit
import json
import glob
import argparse
import functools

from tenk.users import User
import tenk.tkserializer as tkserializer
from tenk.sessions import Session

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

def add_time(choice, time, date=None):
    user = load_user(create=False)
    if user:
        skill = generate_dict(user.get_skill_names())[choice]
        user.add_time(skill, time)
        save(user)
        params = {'skill_name': skill, 'hours': time}
        if date:
            params['session_date'] = date
        session = Session(**params)
        session.serialize_and_save()
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

def add_notes(choice, notes):
    user = load_user(create=False)
    if user:
        skill = generate_dict(user.get_skill_names())[choice]
        session = Session(skill, **notes)
        session.serialize_and_save()
    else:
        print(no_data_msg)

def list_skills():
    """List a user's skills and each skill's number."""
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

def cli_list_handler(args):
    """Handles list-related CLI arguments"""
    if args.skills:
        list_skills()
    elif args.progress:
        print_progress()

def cli_add_handler(args):
    """Handles add-related CLI arguments"""
    if args.time:
        if args.date:
            add_time(args.time[0], float(args.time[1]), args.date)
        else:
            add_time(args.time[0], float(args.time[1]))
    elif args.skill:
        if len(args.skill) == 2:
            add_skill(args.skill[0], float(args.skill[1]))
        else:
            add_skill(args.skill[0])

def cli_del_handler(args):
    """Handles deletion-related CLI arguments"""
    if args.skill:
        remove_skill(args.skill)

def cli_note_handler(args):
    """Handles note-related CLI arguments"""
    notes = dict()
    if args.practiced:
        notes['practiced'] = ' '.join(args.practiced)
    if args.improved:
        notes['improved'] = ' '.join(args.improved)
    if args.future:
        notes['future'] = ' '.join(args.future)
    if args.date:
        notes['session_date'] = args.date
    if notes:
        add_notes(args.skill, notes)

if __name__ == '__main__':
    parser  = argparse.ArgumentParser(prog="python3 -m tenk.main")
    subparsers = parser.add_subparsers(title='subcommands')

    parser_list = subparsers.add_parser('list', aliases=['ls'])
    parser_list.add_argument('-s', '--skills',
                             action='store_true',
                             help="List skillset")
    parser_list.add_argument('-p', '--progress',
                             action='store_true',
                             help="Print progress")
    parser_list.set_defaults(func=cli_list_handler)

    parser_add = subparsers.add_parser('add', aliases=['a'])
    parser_add.add_argument('-s', '--skill',
                            nargs='+',
                            metavar=('name', 'hours'),
                            help="Add skill to skillset")
    parser_add.add_argument('-d', '--date',
                            type=str,
                            help="Custom date: YYYY-MM-DD")
    parser_add.add_argument('-t', '--time',
                            nargs=2,
                            type=float,
                            metavar=('skill', 'time'),
                            help=("Add time to a skill"))
    parser_add.set_defaults(func=cli_add_handler)

    parser_del = subparsers.add_parser('delete', aliases=['del', 'd'])
    parser_del.add_argument('-s', '--skill',
                            type=float,
                            metavar='skill',
                            help="Delete a skill")
    parser_del.set_defaults(func=cli_del_handler)

    parser_note = subparsers.add_parser('note', aliases=['n'])
    parser_note.add_argument('-s', '--skill',
                             type=float,
                             metavar='skill',
                             required=True,
                             help="Skill to add note to")
    parser_note.add_argument('-d', '--date',
                             type=str,
                             help="Custom date: YYYY-MM-DD")
    parser_note.add_argument('-p', '--practiced',
                             nargs='+',
                             metavar='notes',
                             help="Note details about what was practiced")
    parser_note.add_argument('-i', '--improved',
                             nargs='+',
                             metavar='notes',
                             help="Note details about what improved")
    parser_note.add_argument('-f', '--future',
                             nargs='+',
                             metavar='notes',
                             help="Note focus of next practice")
    parser_note.set_defaults(func=cli_note_handler)

    cli_args = parser.parse_args()
    cli_args.func(cli_args)
