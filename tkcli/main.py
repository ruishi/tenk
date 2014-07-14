#!/usr/bin/env python3
"""CLI interface for tenk"""

import argparse
import configparser
import re

from tenk import utils
from tenk.sessions import Session
from tenk.sessionviewer import SessionViewer

no_data_msg = "You have no data!"
config = configparser.ConfigParser(allow_no_value=True)

def add_skill(name, hours=0):
    user = utils.load_user(create=True, config=config)
    user.add_skill(name, hours)
    utils.save(user, config)

def remove_skill(skill):
    user = utils.load_user(config=config)
    if user:
        user.remove_skill(skill)
        utils.save(user, config)
    else:
        print(no_data_msg)

def add_time(skill, time, date=None):
    user = utils.load_user(config=config)
    if user:
        user.add_time(skill, time)
        utils.save(user, config)
        params = {'skill_name': skill, 'hours': time,
                  'file_path': config['PATHS']['sessions_filepath']}
        if date:
            params['session_date'] = date
        session = Session(**params)
        session.serialize_and_save()
    else:
        print(no_data_msg)

def add_notes(skill, notes):
    user = utils.load_user(create=False, config=config)
    if user:
        sessions_filepath = config['PATHS']['sessions_filepath']
        session = Session(skill, file_path=sessions_filepath,
                          **notes)
        session.serialize_and_save()
        print(session)
    else:
        print(no_data_msg)

def get_skill_choice(choice):
    user = utils.load_user(config=config)
    if user:
        skill = generate_dict(user.get_skill_names())[choice]
        return skill
    else:
        return None

def generate_dict(xs):
    """Creates a dictionary where the key is a string representing
    a number and the value is an element of xs"""
    return {float(i + 1):xs[i] for i in range(len(xs))}

def list_skills():
    """List a user's skills and each skill's number."""
    user = utils.load_user(config=config)
    if user:
        for idx, skill in enumerate(user.get_skill_names()):
            print("{}. {}".format(idx + 1, skill))
    else:
        print(no_data_msg)

def print_progress():
    """Print a user's progress"""
    user = utils.load_user(config=config)
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
        skill = get_skill_choice(args.time[0])
        if args.date:
            add_time(skill=skill, time=float(args.time[1]),
                           date=args.date)
        else:
            add_time(skill=skill, time=float(args.time[1]))
    elif args.skill:
        if len(args.skill) == 2:
            add_skill(name=args.skill[0], hours=float(args.skill[1]))
        else:
            add_skill(name=args.skill[0])

def cli_del_handler(args):
    """Handles deletion-related CLI arguments"""
    if args.skill:
        skill = get_skill_choice(choice=args.skill)
        remove_skill(skill=skill)

def get_note_pairs(notes):
    """Use regex to put create tuples of note category and content"""
    note_re = r'(\w+)\s*[=:]\s*(.+?)(?=\s+\w+\s*[=:]|$)'
    return re.findall(note_re, notes, re.VERBOSE)

def cli_note_handler(args):
    """Handles note-related CLI arguments"""
    skill = get_skill_choice(choice=args.skill)
    # argparse returns a list of strings, so they need to be
    # joined into one string
    note_input = ' '.join(args.notes)
    if '=' not in note_input and ':' not in note_input:
        notes = {'notes': note_input}
    else:
        notes = dict()
        note_pairs = get_note_pairs(note_input)
        note_categories = list(config['NOTE CATEGORIES'].keys())
        for pair in note_pairs:
            if pair[0] in note_categories:
                notes[pair[0]] = pair[1]
            else:
                print("{} is not a defined note category.".format(pair[0]))
    if args.date:
        notes['session_date'] = args.date
    if notes:
        add_notes(skill, notes)

def cli_view_handler(args):
    skill = get_skill_choice(choice=args.skill)
    sessions_filepath = config['PATHS']['sessions_filepath']
    session_viewer = SessionViewer(skill, sessions_filepath)
    if args.date:
        session_viewer.print_session(args.date)
    else:
        session_viewer.print_recent()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="python3 -m tenk.main")
    parser.add_argument('-c', '--configfile',
                        nargs='?',
                        default='default.config')

    date_parser = argparse.ArgumentParser(add_help=False)
    date_parser.add_argument('-d', '--date',
                            type=str,
                            help="Custom date: YYYY-MM-DD")

    subparsers = parser.add_subparsers(title='subcommands')

    parser_list = subparsers.add_parser('list', aliases=['ls'])
    parser_list.add_argument('-s', '--skills',
                             action='store_true',
                             help="List skillset")
    parser_list.add_argument('-p', '--progress',
                             action='store_true',
                             help="Print progress")
    parser_list.set_defaults(func=cli_list_handler)

    parser_add = subparsers.add_parser('add', aliases=['a'],
                                       parents=[date_parser])
    parser_add.add_argument('-s', '--skill',
                            nargs='+',
                            metavar=('name', 'hours'),
                            help="Add skill to skillset")
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

    parser_note = subparsers.add_parser('note', aliases=['n'],
                                        parents=[date_parser])
    parser_note.add_argument('-s', '--skill',
                             type=float,
                             metavar='skill',
                             required=True,
                             help="Skill to add note to")
    parser_note.add_argument('notes',
                             nargs='+')
    parser_note.set_defaults(func=cli_note_handler)

    parser_view = subparsers.add_parser('view', aliases=['v'],
                                        parents=[date_parser])
    parser_view.add_argument('-s', '--skill',
                             type=float,
                             metavar='skill',
                             required=True,
                             help='Skill to view session data for')
    parser_view.set_defaults(func=cli_view_handler)

    cli_args = parser.parse_args()

    config.read(cli_args.configfile)
    cli_args.func(cli_args)
