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
    kwargs (dict) - extra note nodes
    """

    def __init__(self, skill_name, file_path, hours=None, session_date=None,
                 **kwargs):
        self.skill_name = skill_name
        self.hours = hours
        if session_date:
            session_date = [int(d) for d in session_date.split('-')]
            self.session_date = date(*session_date)
        else:
            self.session_date = date.today()
        self.notes = kwargs
        self.file_path = file_path

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
        for k, v in self.notes.items():
            note_node = etree.SubElement(session_node, k)
            note_node.text = v
        return root

    def update_xml(self, session_node, separator='<br/>'):
        """Update XML for existing session"""
        hours_node = session_node.find('hours')
        if hours_node is not None and self.hours:
            hours_node.text = str(float(hours_node.text) + self.hours)
        elif self.hours:
            hours_node = etree.SubElement(session_node, 'hours')
            hours_node.text = str(self.hours)

        for k, v in self.notes.items():
            note_node = session_node.find(k)
            if note_node is None:
                note_node = etree.SubElement(session_node, k)
            if note_node.text is not None:
                note_node.text = separator.join([note_node.text, v])
            else:
                note_node.text = v
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

    def __repr__(self):
        """Representation of session object.

        This only includes the data necessary to identify the session,
        i.e., skill name and session date."""

        return 'Session(skill_name={}, session_date={})'.format(self.skill_name,
                                                                str(self.session_date))

    def __str__(self):
        note_strs = ["{}: {}".format(k, v) for k,v in self.notes.items()]
        note_final_string = '\n'.join(note_strs)
        string_rep = ("{}\n{}\n"
                      "Date: {}\n"
                      "{}".format(self.skill_name,
                                  '-' * len(self.skill_name),
                                  str(self.session_date),
                                  note_final_string))
        return string_rep
