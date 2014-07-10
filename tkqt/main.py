#!/usr/bin/env python3

import sys
import configparser

from tenk import utils

from PySide.QtCore import *
from PySide import QtGui


class Form(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.user = utils.load_user(create=False)
        if self.user.skillset:
            self.existing_user_setup()
        else:
            self.new_user_setup()

    def new_user_setup(self):
        self.setWindowTitle("tenk")
        self.label = QtGui.QLabel("Pending")
        self.button = QtGui.QPushButton("OK")

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def existing_user_setup(self):
        self.setWindowTitle("tenk")
        layout = QtGui.QVBoxLayout()
        self.skill_widgets = dict()
        for skill in self.user.skillset:
            name_label = QtGui.QLabel(skill.name)
            level_label = QtGui.QLabel("Level {}".format(skill.calc_level()))
            level_label.setAlignment(Qt.AlignRight)
            progress_bar = QtGui.QProgressBar()
            progress_bar.setValue(skill.calc_progress())
            self.skill_widgets[skill.name] = (level_label,
                                              progress_bar)
            hbox = QtGui.QHBoxLayout()
            hbox.addWidget(name_label)
            hbox.addWidget(level_label)
            layout.addLayout(hbox)
            layout.addWidget(progress_bar)

        self.setLayout(layout)

#        self.button.clicked.connect(self.greetings)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
