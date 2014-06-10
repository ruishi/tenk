tenk
====
tenk is a program inspired from the "10,000-Hour Rule," which claims
that 10,000 hours of practice is needed to master a particular
skill. tenk helps track the amount of time spent practicing each
skill. It features a leveling system and can print a visual
representation of a user's progress.

Usage
=====
tenk is a CLI application. You can run the application with `python3
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
tenk requires lxml for the serialization of session data.
