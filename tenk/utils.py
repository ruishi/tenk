"""Utility functions utilized by multiple files"""
import os
import json

from tenk.users import User
import tenk.tkserializer as tkserializer
from tenk.sessions import Session
import configparser

config = configparser.ConfigParser(allow_no_value=True)

no_data_msg = "You have no data!"

def save(user, configfile='default.config'):
    config.read(configfile)
    u_file = config['PATHS']['user_filepath']
    with open(u_file, encoding='utf-8', mode='w') as f:
        json.dump(user, f, indent=2, default=tkserializer.to_json)

def load_user(create=False, configfile='default.config'):
    """Load a user's tk file into a User object. If create is True,
    then a user object will be created if no tk file exists."""
    config.read(configfile)
    tk_dir = config['PATHS']['tk_dir']
    if os.path.exists(tk_dir):
        u_file = config['PATHS']['user_filepath']
        with open(u_file, encoding='utf-8', mode='r') as f:
            user = json.load(f, object_hook=tkserializer.from_json)
        return user
    else:
        if create:
            os.makedirs(tk_dir)
            u_file = config['PATHS']['user_filepath']
            open(u_file, 'a').close()
            return User("Default")
        else:
            return None

def add_time(skill, time, date=None, configfile='default.config'):
    user = load_user(configfile=configfile)
    if user:
        user.add_time(skill, time)
        save(user, configfile)
        config.read(configfile)
        params = {'skill_name': skill, 'hours': time,
                  'file_path': config['PATHS']['sessions_filepath']}
        if date:
            params['session_date'] = date
        session = Session(**params)
        session.serialize_and_save()
    else:
        print(no_data_msg)

def add_skill(name, hours=0, configfile='default.config'):
    user = load_user(create=True, configfile=configfile)
    user.add_skill(name, hours)
    save(user, configfile)

def remove_skill(skill, configfile='default.config'):
    user = load_user(configfile=configfile)
    if user:
        user.remove_skill(skill)
        save(user, configfile)
    else:
        print(no_data_msg)

def add_notes(skill, notes, configfile='default.config'):
    user = load_user(create=False, configfile=configfile)
    if user:
        config.read(configfile)
        sessions_filepath = config['PATHS']['sessions_filepath']
        session = Session(skill, file_path=sessions_filepath,
                          **notes)
        session.serialize_and_save()
    else:
        print(no_data_msg)
