"""Utility functions utilized by multiple files"""
import os
import json

from tenk.users import User
import tenk.tkserializer as tkserializer
from tenk.sessions import Session

def save(user, config):
    u_file = config['PATHS']['user_filepath']
    with open(u_file, encoding='utf-8', mode='w') as f:
        json.dump(user, f, indent=2, default=tkserializer.to_json)

def load_user(config, create=False):
    """Load a user's tk file into a User object. If create is True,
    then a user object will be created if no tk file exists."""
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
