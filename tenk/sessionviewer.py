"""Pulls desired sessions for viewing"""

from lxml import etree
from tenk.sessions import Session

class SessionViewer:
    def __init__(self, skill, file_path):
        self.skill = skill
        with open(file_path) as f:
            parser = etree.XMLParser(remove_blank_text=True)
            root = etree.parse(f, parser).getroot()
        self.subtree = root.find('skill[@name="{}"]'.format(skill))

    def get_session(self, date):
        """Returns session data for given date if it exists. Otherwise returns
        None."""
        if self.subtree is None:
            print("{} is not in your skillset".format(self.skill))
            return None
        else:
            return self.subtree.find('session[@date="{}"]'.format(date))

    def get_recent(self):
        """Returns data for up to the last 5 recent sessions"""
        if self.subtree is None:
            print("{} is not in your skillset".format(self.skill))
            return None
        else:
            return self.subtree.findall('session')[-5:]

    def print_session(self, date):
        session_node = self.get_session(date)
        if session_node is not None:
            session = Session.deserialize(self.skill, session_node)
            print(session)
        else:
            print("No session data for that date exists!")

    def print_recent(self):
        recent_session_nodes = self.get_recent()
        if recent_session_nodes:
            for session_node in recent_session_nodes:
                session = Session.deserialize(self.skill, session_node)
                print(session)
        else:
            print("No session data exists for {}".format(self.skill))
