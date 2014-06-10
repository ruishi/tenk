import os
import glob
import json

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
        if create:
            os.makedirs(os.path.join(os.path.expanduser('~'), 'tenk'))
            u_file = os.path.join(os.path.expanduser('~'),
                                  'tenk/default.tk')
            open(u_file, 'a').close()
            return User("Default")
        else:
            return None

def add_time(skill, time, date=None):
    user = load_user()
    if user:
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

def remove_skill(skill):
    user = load_user()
    if user:
        user.remove_skill(skill)
        save(user)
    else:
        print(no_data_msg)

def add_notes(skill, notes):
    user = load_user(create=False)
    if user:
        session = Session(skill, **notes)
        session.serialize_and_save()
    else:
        print(no_data_msg)
