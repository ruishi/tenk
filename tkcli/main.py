#!/usr/bin/env python3
"""CLI interface for tenk"""

import argparse
import configparser
import re

from tenk import utils

def get_skill_choice(choice, configfile='default.config'):
    user = utils.load_user(configfile=configfile)
    if user:
        skill = generate_dict(user.get_skill_names())[choice]
        return skill
    else:
        return None

def generate_dict(xs):
    """Creates a dictionary where the key is a string representing
    a number and the value is an element of xs"""
    return {float(i + 1):xs[i] for i in range(len(xs))}

def list_skills(configfile='default.config'):
    """List a user's skills and each skill's number."""
    user = utils.load_user(configfile=configfile)
    if user:
        for idx, skill in enumerate(user.get_skill_names()):
            print("{}. {}".format(idx + 1, skill))
    else:
        print(utils.no_data_msg)

def print_progress(configfile='default.config'):
    """Print a user's progress"""
    user = utils.load_user(configfile=configfile)
    if user:
        user.print_progress()
    else:
        print(utils.no_data_msg)

def cli_list_handler(args):
    """Handles list-related CLI arguments"""
    if args.skills:
        list_skills(configfile=args.configfile)
    elif args.progress:
        print_progress(configfile=args.configfile)


def cli_add_handler(args):
    """Handles add-related CLI arguments"""
    if args.time:
        skill = get_skill_choice(args.time[0], configfile=args.configfile)
        if args.date:
            utils.add_time(skill=skill, time=float(args.time[1]),
                           date=args.date, configfile=args.configfile)
        else:
            utils.add_time(skill=skill, time=float(args.time[1]),
                           configfile=args.configfile)
    elif args.skill:
        if len(args.skill) == 2:
            utils.add_skill(name=args.skill[0], hours=float(args.skill[1]),
                            configfile=args.configfile)
        else:
            utils.add_skill(name=args.skill[0], configfile=args.configfile)

def cli_del_handler(args):
    """Handles deletion-related CLI arguments"""
    if args.skill:
        skill = get_skill_choice(choice=args.skill,
                                 configfile=args.configfile)
        utils.remove_skill(skill=skill, configfile=args.configfile)

def get_note_pairs(notes):
    """Use regex to put create tuples of note category and content"""
    note_re = r'(\w+)\s*[=:]\s*(.+?)(?=\s+\w+\s*[=:]|$)'
    return re.findall(note_re, notes, re.VERBOSE)

def cli_note_handler(args):
    """Handles note-related CLI arguments"""
    skill = get_skill_choice(choice=args.skill, configfile=args.configfile)
    # argparse returns a list of strings, so they need to be
    # joined into one string
    note_input = ' '.join(args.notes)
    if '=' not in note_input and ':' not in note_input:
        notes = {'notes': note_input}
    else:
        notes = dict()
        note_pairs = get_note_pairs(note_input)
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(args.configfile)
        note_categories = list(config['NOTE CATEGORIES'].keys())
        for pair in note_pairs:
            if pair[0] in note_categories:
                notes[pair[0]] = pair[1]
            else:
                print("{} is not a defined note category.".format(pair[0]))
    if args.date:
        notes['session_date'] = args.date
    if notes:
        utils.add_notes(skill, notes, configfile=args.configfile)

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

    cli_args = parser.parse_args()

    cli_args.func(cli_args)
