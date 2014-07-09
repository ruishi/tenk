tenk
====
tenk is a program inspired from the "10,000-Hour Rule," which claims
that 10,000 hours of practice is needed to master a particular
skill. tenk helps track the amount of time spent practicing each
skill. It features a leveling system and can print a visual
representation of a user's progress.

Usage
=====
tenk is a CLI application. To use tenk, the first thing you must do is
set up the configuration file. A sample configuration file is
included. The `PATHS` section must be modified for tenk to work. By
default, tenk will look for a configuration file called
`default.config`. You can point it to a different file with the `-c`
or `--configfile` flag.

You can run the application with `python3
-m tenk.main`, assuming that you are in the top level project
directory. You can also run `tenk.sh`

Usage Examples
--------------
**List your skills:**
```sh
$ ./tenk.sh ls -s
1. programming
2. french
3. piano
```

**List your progress:**
```sh
$ ./tenk.sh ls -p
programming (600.0 hours, level 6):
 [                                                  ] 0.0%
french (118.0 hours, level 1):
 [:::::::::                                         ] 18.0%
piano (15.5 hours, level 0):
 [:::::::                                           ] 15.5%
```

**Add and remove skills:**
```sh
$ ./tenk.sh add -s chinese
$ ./tenk.sh ls -s
1. programming
2. french
3. piano
4. chinese

$ ./tenk.sh del -s 4
$ ./tenk.sh ls -s
1. programming
2. french
3. piano

$ ./tenk.sh add chinese 30
$ ./tenk.sh ls -p
programming (600.0 hours, level 6):
 [                                                  ] 0.0%
french (118.0 hours, level 1):
 [:::::::::                                         ] 18.0%
piano (15.5 hours, level 0):
 [:::::::                                           ] 15.5%
chinese (30 hours, level 0):
 [:::::::::::::::                                   ] 30%
 ```

In general when you modify any skill, you need to use it's skill
number.

**Add time:**
```sh
$ ./tenk.sh ls -s
1. programming
2. french
3. piano
4. chinese
5. tagalog

$ ./tenk.sh add -t 1 3
```

**Add some notes:**
```sh
$ ./tenk.sh note -s 1 improved = regular expressions future = basic frontend development
programming
-----------
Date: 2014-07-07
future: basic frontend development
improved: regular expressions
```

Here I use the note categories `future` and `improved` which I've
defined in my default.config file. If you use a note category that
doesn't exist, the note will not be saved. If you don't use a note
category at all, tenk will save the note in a node called `notes`.

**View notes:**
```sh
$ ./tenk.sh view -s 3
piano
-----
Date: 2014-06-09
improved: chord transitions
future: major triads and major chord inversions
learned: chord inversions
piano
-----
Date: 2014-06-11
improved: chord transitions, hand independence
learned: chord inversions, hand independence with amazing grace
piano
-----
Date: 2014-06-15
improved: triads
future: let it be
learned: triads, moving in thirds, let it be
piano
-----
Date: 2014-06-16
improved: let it be, moving in thirds
future: appregios
learned: let it be, triads, moving in thirds, triplets, appregios
piano
-----
Date: 2014-06-17
improved: old school triplets, appregios,
future: chords and their inversions
learned: old school triplets, old school triplets version for small hands, appregio version of first chord progresion, f major scale left and right hand

$ ./tenk.sh view -s 3 -d 2014-06-15
piano
-----
Date: 2014-06-15
improved: triads
future: let it be
learned: triads, moving in thirds, let it be
```

The view command displays session data for up to the 5 most recent
dates. You can view the data for a specific date by using the `--date`
or `-d` flag.

Development
===========
tenk was developed using Python 3 and is not compatible with Python
2.7. Feature development is done on the "dev" branch.

To run the unit tests, cd to the parent directory and run
`runtests.sh`. runtests.sh will take one parameter, so for instance
you can run `./runtests.sh -v` for verbose output.

To run a single test, just execute it directly. For example, `python3
-m tests.skills_tests`

Dependencies
------------
+ **lxml** for data serialization
+ **PySide** for the GUI wrapper (coming soon!)
