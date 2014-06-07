"""Session class for logging practice details"""

import os
from datetime import date
from lxml import etree

class Session:
    """Holds practice session data.

    Attributes:
    skill_name (str) -- name of the skill being practiced
    hours (float) -- the amount of hours spent on the practice session
    session_date (datetime.date) -- the date of the practice session
    practiced (str) -- optional, what was practiced
    improved (str) -- optional, what improved from last time
    future (str) -- optional, what to focus on in future sessions"""

    def __init__(self, skill_name, hours, session_date=None,
                 practiced=None, improved=None, future=None,
                 file_path=None):
        self.skill_name = skill_name
        self.hours = hours
        if session_date:
            self.session_date = session_date
        else:
            self.session_date = date.today()
        if practiced:
            self.practiced = practiced
        if improved:
            self.improved = improved
        if future:
            self.future = future
        if file_path:
            self.file_path = file_path
        else:
            self.file_path = os.path.join(os.path.expanduser('~'),
                                          'tenk/default.xml')

    def has_save_file(self):
        """Returns True if sessions XML file exists, False otherwise"""
        return os.path.isfile(self.file_path)

    def generate_xml(self):
        """Generate XML for the session."""
        if self.has_save_file():
            with open(self.file_path) as f:
                root = etree.parse(f)
            if not root.find('skill[@name="{}"]'.format(self.skill_name)):
                skill_node = etree.SubElement(root, 'skill',
                                              name=self.skill_name)
        else:
            root = etree.Element('sessions')
            skill_node = etree.SubElement(root, 'skill', name=self.skill_name)

        session_node = etree.SubElement(skill_node, 'session')
        date_node = etree.SubElement(session_node, 'date')
        date_node.text = str(self.session_date)
        time_node = etree.SubElement(session_node, 'hours')
        time_node.text = str(self.hours)
        if self.practiced:
            practiced_node = etree.SubElement(session_node, 'practiced')
            practiced_node.text = self.practiced
        if self.improved:
            improved_node = etree.SubElement(session_node, 'improved')
            improved_node.text = self.improved
        if self.future:
            future_node = etree.SubElement(session_node, 'future')
            future_node.text = self.future

        return root

    def save(self, root):
        """Save XML tree to file."""
        xml = etree.tostring(root, pretty_print=True, xml_declaration=True)
        xml = xml.decode('utf-8')
        with open(self.file_path, 'w') as f:
            f.write(xml)
