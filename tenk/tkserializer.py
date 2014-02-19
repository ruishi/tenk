#!/usr/bin/env python3
################################################################################
#author: RD Galang
#description: Custom JSON serializer for User class
################################################################################
import json
from users import User
from skills import Skill

def to_json(obj):
    if isinstance(obj, User):
        return {'__class__': 'User',
                'name': obj.name,
                'skills': obj.skillset
                }
    if isinstance(obj, Skill):
        return {'__class__': 'Skill',
                'name': obj.name,
                'hours': obj.hours
                }
    raise TypeError(repr(obj) + " is not Python serializable")

def from_json(obj):
    if '__class__' in obj:
        if obj['__class__'] == 'User':
            user = User(obj['name'])
            user.skillset = obj['skills']
            return user
        if obj['__class__'] == 'Skill':
            return Skill(obj['name'], obj['hours'])
    return obj
