# coding: utf-8
"""
turktools tests
mitcho (Michael Yoshitaka Erlewine), mitcho@mitcho.com, May 2013

The MIT License (MIT)
Copyright (c) 2013 Michael Yoshitaka Erlewine
See readme for license block
"""

from __future__ import print_function
import unittest, sys
# todo: import doctest



runner = unittest.TextTestRunner(verbosity=1 + sys.argv.count('-v'))
suite = unittest.TestLoader().loadTestsFromNames([
	'tests.test_shared',
	'tests.test_lister',
	'tests.test_templater',
	'tests.test_decoder',
])
raise SystemExit(not runner.run(suite).wasSuccessful())
