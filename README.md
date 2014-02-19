TenK
====
TenK is a program inspired from the "10,000-Hour Rule," which claims that 10,000 hours of practice is needed to master a particular skill. TenK helps track the amount of time spent practicing each skill. It features a leveling system and can print a visual representation of a user's progress.

Usage
=====
TenK is a CLI application. It can be run by executing main.py. A GUI wrapper is currently in development.

Development
===========
TenK was developed using Python 3.3 and is not compatible with Python 2.7. Feature development is done on the "dev" branch and GUI development is done on the "gui" branch.

To run the unit tests, navigate to the parent directory from the command line and enter:
```
python -m unittest discover . "*_test.py"
```