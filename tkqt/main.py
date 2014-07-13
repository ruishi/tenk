#!/usr/bin/env python3

import sys
import configparser
from collections import namedtuple

from tenk import utils

from PySide.QtCore import *
from PySide import QtGui

LPWidgets = namedtuple('LPWidgets', ['level_label',
                                     'progress_bar',
                                     'add_button'])

class Form(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.user = utils.load_user(create=False)
        self.setup_ui()

    def setup_ui(self):
        self.setup_add_skill_win()
        self.setup_add_time_win()
        self.setup_main_win()
        self.setup_bottom_bar()

    def setup_main_win(self):
        self.setWindowTitle("tenk")

        self.bottom_bar_layout = QtGui.QVBoxLayout()
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
        self.skill_widgets = dict()
        for skill in self.user.skillset:
            self.add_skill_to_main_win(skill.name,
                                       skill.calc_level(),
                                       skill.calc_progress())

        self.layout.addLayout(self.main_view_layout)
        self.setLayout(self.layout)

    def setup_bottom_bar(self):
        self.add_skill_btn = QtGui.QPushButton('Add skill')
        self.bottom_bar_layout.addWidget(self.add_skill_btn)
        self.add_skill_btn.clicked.connect(self.add_skill_win.show)
        self.layout.addLayout(self.bottom_bar_layout)

    def setup_add_skill_win(self):
        self.add_skill_win = QtGui.QWidget()
        self.add_skill_win.setWindowTitle("tenk: Add new skill")

        self.skill_name_input = QtGui.QLineEdit()
        self.hours_input = QtGui.QLineEdit('0')
        self.as_submit_btn = QtGui.QPushButton('Add')
        self.as_submit_btn.clicked.connect(self.add_skill)

        as_win_layout = QtGui.QFormLayout()
        as_win_layout.addRow(self.tr("&Skill name:"), self.skill_name_input)
        as_win_layout.addRow(self.tr("&Initial hours:"), self.hours_input)
        as_win_layout.addRow(self.as_submit_btn)
        self.add_skill_win.setLayout(as_win_layout)

    def add_skill_to_main_win(self, skill_name, skill_level, skill_progress):
        name_label = QtGui.QLabel(skill_name)
        level_label = QtGui.QLabel("Level {}".format(skill_level))
        level_label.setAlignment(Qt.AlignRight)
        progress_bar = QtGui.QProgressBar()
        progress_bar.setValue(skill_progress)
        add_button = QtGui.QPushButton('+')
        add_button.clicked.connect(self.add_time_win.show)
        self.skill_widgets[skill_name] = LPWidgets(level_label,
                                                   progress_bar,
                                                   add_button)
        # horizontal box for name and level
        nl_splitter = QtGui.QSplitter()
        nl_splitter.addWidget(name_label)
        nl_splitter.addWidget(level_label)
        self.main_view_layout.addWidget(nl_splitter)

        # horizontal box for progress bar and add button
        pa_splitter = QtGui.QSplitter()
        pa_splitter.addWidget(progress_bar)
        pa_splitter.addWidget(add_button)
        self.main_view_layout.addWidget(pa_splitter)


    def setup_add_time_win(self):
        self.add_time_win = QtGui.QWidget()
        self.add_time_win.setWindowTitle("tenk: Add practice time")

        self.skill_cb = QtGui.QComboBox()
        self.skill_cb.addItems(self.user.get_skill_names())

        self.at_win_layout = QtGui.QVBoxLayout()
        self.at_win_layout.addWidget(self.skill_cb)
        self.add_time_win.setLayout(self.at_win_layout)

    def add_skill(self):
        skill_name = self.skill_name_input.text()
        hours = self.hours_input.text()
        if not skill_name:
            message_box = QtGui.QMessageBox()
            message_box.setText("Please enter a skill name.")
            message_box.exec_()
        else:
            try:
                hours = float(hours)
                skill = utils.add_skill(skill_name, hours)
                self.add_skill_to_main_win(skill_name,
                                           skill.calc_level(),
                                           skill.calc_progress())
                self.setLayout(self.layout)
                self.add_skill_win.hide()
            except ValueError:
                message_box = QtGui.QMessageBox()
                message_box.setText("{} is not a valid number.".format(hours))
                message_box.exec_()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
