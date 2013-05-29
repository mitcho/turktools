# coding: utf-8
"""
turk tools tests
mitcho (Michael Yoshitaka Erlewine), mitcho@mitcho.com, May 2013

The MIT License (MIT)
Copyright (c) 2013 Michael Yoshitaka Erlewine
See readme for license block
"""

from __future__ import print_function
import unittest, sys
# todo: import doctest
import tests.test_decoder

runner = unittest.TextTestRunner(verbosity=1 + sys.argv.count('-v'))
suite = unittest.TestLoader().loadTestsFromNames([
	'tests.test_decoder',
	'tests.test_lister',
])
raise SystemExit(not runner.run(suite).wasSuccessful())
