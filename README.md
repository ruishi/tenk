tenk
====
tenk is a program inspired from the "10,000-Hour Rule," which claims that 10,000 hours of practice is needed to master a particular skill. tenk helps track the amount of time spent practicing each skill. It features a leveling system and can print a visual representation of a user's progress.

Usage
=====
tenk is a CLI application. It can be run by executing main.py. A GUI wrapper is in the works.

Development
===========
tenk was developed using Python 3 and is not compatible with Python 2.7. Feature development is done on the "dev" branch.

To run the unit tests, cd to the parent directory and run `runtests.sh`. runtests.sh will take one parameter, so for instance you can run `./runtests.sh -v` for verbose output.

To run a single test, just execute it directly. For example, `python3 -m tests.skills_tests`

Dependencies
------------
tenk requires lxml and pygal for graphing capabilities.
