"""CLI interface for tenk"""

import argparse

from tenk import utils

def get_skill_choice(choice):
    user = utils.load_user()
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
    user = utils.load_user()
    if user:
        for idx, skill in enumerate(user.get_skill_names()):
            print("{}. {}".format(idx + 1, skill))
    else:
        print(utils.no_data_msg)

def print_progress():
    """Print a user's progress"""
    user = utils.load_user()
    if user:
        user.print_progress()
    else:
        print(utils.no_data_msg)

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
            utils.add_time(skill, float(args.time[1]), args.date)
        else:
            utils.add_time(skill, float(args.time[1]))
    elif args.skill:
        if len(args.skill) == 2:
            utils.add_skill(args.skill[0], float(args.skill[1]))
        else:
            utils.add_skill(args.skill[0])

def cli_del_handler(args):
    """Handles deletion-related CLI arguments"""
    if args.skill:
        skill = get_skill_choice(args.skill)
        utils.remove_skill(skill)

def cli_note_handler(args):
    """Handles note-related CLI arguments"""
    skill = get_skill_choice(args.skill)
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
        utils.add_notes(skill, notes)

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
