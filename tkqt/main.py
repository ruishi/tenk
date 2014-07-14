#!/usr/bin/env python3

import sys
import configparser
from collections import namedtuple, OrderedDict
from datetime import date

from tenk import utils
from tenk.sessions import Session

from PySide.QtCore import *
from PySide import QtGui

LPWidgets = namedtuple('LPWidgets', ['level_label',
                                     'progress_bar',
                                     'add_button'])

class Form(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read('default.config')
        self.user = utils.load_user(create=False, config=self.config)
        self.setup_ui()

    def setup_ui(self):
        self.setup_add_skill_win()
        self.setup_add_time_win()
        self.setup_main_win()
        self.setup_switch_win()
        self.setup_bottom_bar()

    def setup_main_win(self):
        self.setWindowTitle("tenk")

        self.bottom_bar_layout = QtGui.QHBoxLayout()
        self.main_view_layout = QtGui.QVBoxLayout()

        self.layout = QtGui.QVBoxLayout()
        if self.user.skillset:
            self.existing_user_setup()
        else:
            self.new_user_setup()

    def new_user_setup(self):
        """If no user data exists, create a blank GUI with a single button
        to add a skill"""
        self.layout.addLayout(self.main_view_layout)
        self.setLayout(self.layout)

    def existing_user_setup(self):
        """If user data exists, then populate main window with progress
        information about each skill"""
        self.skill_widgets = dict()
        for skill in self.user.skillset:
            self.add_skill_to_main_win(skill.name,
                                       skill.calc_level(),
                                       skill.calc_progress())

        self.layout.addLayout(self.main_view_layout)
        self.setLayout(self.layout)

    def setup_bottom_bar(self):
        """Create bottom bar"""
        self.add_skill_btn = QtGui.QPushButton('Add skill')
        self.add_skill_btn.clicked.connect(self.add_skill_win.show)
        self.switch_user_btn = QtGui.QPushButton('Switch user')
        self.switch_user_btn.clicked.connect(self.switch_win.show)

        self.bottom_bar_layout.addWidget(self.add_skill_btn)
        self.bottom_bar_layout.addWidget(self.switch_user_btn)
        self.layout.addLayout(self.bottom_bar_layout)

    def setup_add_skill_win(self):
        """Create input window for adding a skill to a user's skillset"""
        self.add_skill_win = QtGui.QWidget()
        self.add_skill_win.setWindowTitle("tenk: Add new skill")

        self.skill_name_input = QtGui.QLineEdit()
        self.init_hours_input = QtGui.QLineEdit('0')
        self.as_submit_btn = QtGui.QPushButton('Add')
        self.as_submit_btn.clicked.connect(self.add_skill)

        as_win_layout = QtGui.QFormLayout()
        as_win_layout.addRow(self.tr("Skill name:"), self.skill_name_input)
        as_win_layout.addRow(self.tr("Initial hours:"), self.init_hours_input)
        as_win_layout.addRow(self.as_submit_btn)
        self.add_skill_win.setLayout(as_win_layout)

    def setup_switch_win(self):
        self.switch_win = QtGui.QWidget()

    def setup_add_time_win(self):
        """Create input window for adding practice information for a skill"""
        self.add_time_win = QtGui.QWidget()
        self.add_time_win.setWindowTitle("tenk: Add practice time")

        self.skill_cb = QtGui.QComboBox()
        self.skill_cb.addItems(self.user.get_skill_names())
        self.date_edit = QtGui.QDateEdit()
        today = date.today()
        self.date_edit.setMaximumDate(QDate(today.year,
                                            today.month,
                                            today.day))
        self.date_edit.setDate(QDate(today.year,
                                     today.month,
                                     today.day))
        self.hours_input = QtGui.QLineEdit()
        note_categories = list(self.config['NOTE CATEGORIES'].keys())
        # use OrderedDict here so that the order of categories is
        # always the same in the add time window
        self.note_inputs = OrderedDict()
        for note_category in note_categories:
            note_category = '{}:'.format(note_category)
            self.note_inputs[note_category] = QtGui.QTextEdit()
        self.at_submit_btn = QtGui.QPushButton('Submit')
        self.at_submit_btn.clicked.connect(self.add_time)

        at_win_layout = QtGui.QFormLayout()
        at_win_layout.addRow(self.tr("Skill:"), self.skill_cb)
        at_win_layout.addRow(self.tr("Date:"), self.date_edit)
        at_win_layout.addRow(self.tr("Hours:"), self.hours_input)
        for category, text_edit in self.note_inputs.items():
            at_win_layout.addRow(self.tr(category), text_edit)
        at_win_layout.addRow(self.at_submit_btn)
        self.add_time_win.setLayout(at_win_layout)

    def show_add_time_win(self, skill_name):
        """Displays the add time window with appropriate skill selected"""
        index = self.skill_cb.findText(skill_name)
        self.skill_cb.setCurrentIndex(index)
        self.add_time_win.show()

    def add_skill_to_main_win(self, skill_name, skill_level, skill_progress):
        """Add skill data to main window"""
        name_label = QtGui.QLabel(skill_name)
        level_label = QtGui.QLabel("Level {}".format(skill_level))
        level_label.setAlignment(Qt.AlignRight)
        progress_bar = QtGui.QProgressBar()
        progress_bar.setValue(skill_progress)
        add_button = QtGui.QPushButton('+')
        add_button.clicked.connect(lambda: self.show_add_time_win(skill_name))
        self.skill_widgets[skill_name] = LPWidgets(level_label,
                                                   progress_bar,
                                                   add_button)
        # splitter for name and level
        nl_splitter = QtGui.QSplitter()
        nl_splitter.addWidget(name_label)
        nl_splitter.addWidget(level_label)
        self.main_view_layout.addWidget(nl_splitter)

        # splitter for progress bar and add button
        pa_splitter = QtGui.QSplitter()
        pa_splitter.addWidget(progress_bar)
        pa_splitter.addWidget(add_button)
        self.main_view_layout.addWidget(pa_splitter)

    def add_skill(self):
        """Add skill to skillset using data from add_skill_win"""
        skill_name = self.skill_name_input.text()
        hours = self.init_hours_input.text()
        if not skill_name:
            message_box = QtGui.QMessageBox()
            message_box.setText("Please enter a skill name.")
            message_box.exec_()
        else:
            try:
                hours = float(hours)
                skill = self.user.add_skill(skill_name, hours)
                utils.save(self.user, self.config)
                self.add_skill_to_main_win(skill_name,
                                           skill.calc_level(),
                                           skill.calc_progress())
                self.setLayout(self.layout)
                self.add_skill_win.hide()
                self.reset_add_skill_win()
            except ValueError:
                message_box = QtGui.QMessageBox()
                message_box.setText("{} is not a valid number.".format(hours))
                message_box.exec_()

    def add_time(self):
        hours = self.hours_input.text()
        try:
            hours = float(hours)

            skill_name = self.skill_cb.currentText()
            session_date = self.date_edit.date().toString('yyyy-M-dd')
            file_path = self.config['PATHS']['sessions_filepath']
            session_params = {'skill_name': skill_name,
                              'session_date': session_date,
                              'hours': hours,
                              'file_path': file_path}

            for note_category, text_edit in self.note_inputs.items():
                # adding notes is optional, so ignore textareas left blank
                note_text = text_edit.toPlainText()
                if note_text:
                    session_params[note_category.replace(':','')] = note_text
            session = Session(**session_params)
            session.serialize_and_save()

            self.user.add_time(skill_name, hours)
            utils.save(self.user, self.config)
            self.add_time_win.hide()
            self.reset_add_time_win()
        except ValueError as e:
            message_box = QtGui.QMessageBox()
            message_box.setText(e)
            message_box.exec_()

    def reset_add_skill_win(self):
        self.skill_name_input.clear()
        self.init_hours_input.setText('0')

    def reset_add_time_win(self):
        self.hours_input.clear()
        today = date.today()
        self.date_edit.setDate(QDate(today.year,
                                     today.month,
                                     today.day))
        for _, text_edit in self.note_inputs.items():
            text_edit.clear()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
