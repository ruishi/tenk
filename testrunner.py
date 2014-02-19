#!usr/bin/env python3
################################################################################
#author: RD Galang
#description: Runs all unit tests
################################################################################
import unittest
import os, sys
srcdir= 'tenk'
sys.path.insert(0,os.path.abspath(os.path.join(srcdir)))

if __name__ == '__main__':
    suite = unittest.TestLoader().discover('.', pattern = '*_test.py')
    unittest.TextTestRunner(verbosity=2).run(suite)
