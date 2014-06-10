"""Session class for logging practice details"""

import os
from datetime import date
from lxml import etree

class Session:
    """Holds practice session data.

    Attributes:
    skill_name (str) -- name of the skill being practiced
    hours (float) -- optional, the amount of hours spent on the
                     practice session
    session_date (datetime.date) -- the date of the practice session
    practiced (str) -- optional, what was practiced
    improved (str) -- optional, what improved from last time
    future (str) -- optional, what to focus on in future sessions

    """

    def __init__(self, skill_name, hours=None, session_date=None,
                 practiced=None, improved=None, future=None,
                 file_path=None):
        self.skill_name = skill_name
        self.hours = hours
        if session_date:
            session_date = [int(d) for d in session_date.split('-')]
            self.session_date = date(*session_date)
        else:
            self.session_date = date.today()
        self.practiced = practiced
        self.improved = improved
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
                parser = etree.XMLParser(remove_blank_text=True)
                root = etree.parse(f, parser).getroot()
            skill_node = root.find('skill[@name="{}"]'.format(self.skill_name))
            if skill_node is not None:
                session_node = self.find_existing_session(skill_node)
                if session_node is not None:
                    session_node = self.update_xml(session_node)
                    return root
            else:
                skill_node = etree.SubElement(root, 'skill',
                                              name=self.skill_name)
        else:
            root = etree.Element('sessions')
            skill_node = etree.SubElement(root, 'skill',
                                          name=self.skill_name)

        session_node = etree.SubElement(skill_node, 'session',
                                        date=str(self.session_date))
        if self.hours:
            hours_node = etree.SubElement(session_node, 'hours')
            hours_node.text = str(self.hours)
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

    def update_xml(self, session_node, separator='<br/>'):
        """Update XML for existing session"""
        hours_node = session_node.find('hours')
        if hours_node is not None and self.hours:
            hours_node.text = str(float(hours_node.text) + self.hours)
        else:
            hours_node = etree.SubElement(session_node, 'hours')
            hours_node.text = str(self.hours)

        detail_tuples = [('practiced', self.practiced),
                         ('improved', self.improved),
                         ('future', self.future)]
        for detail in detail_tuples:
            if detail[1]:
                detail_node = session_node.find(detail[0])
                if detail_node is None:
                    detail_node = etree.SubElement(session_node, detail[0])
                if detail_node.text is not None:
                    detail_node.text = separator.join([detail_node.text,
                                                       detail[1]])
                else:
                    detail_node.text = detail[1]
        return session_node

    def find_existing_session(self, skill_node):
        """Returns the session node if data has already been logged,
        otherwise returns None."""
        if skill_node is None:
            return None
        return skill_node.find('session[@date="{}"]'.format(self.session_date))

    def save(self, root):
        """Save XML tree to file."""
        xml = etree.tostring(root, encoding='utf-8', pretty_print=True,
                             xml_declaration=True)
        xml = xml.decode('utf-8')
        with open(self.file_path, 'w') as f:
            f.write(xml)

    def serialize_and_save(self):
        """Serialize data into XML and save to file"""
        root = self.generate_xml()
        self.save(root)
