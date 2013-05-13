# coding: utf-8
"""
turk tools tests
mitcho (Michael Yoshitaka Erlewine), mitcho@mitcho.com, May 2013

The MIT License (MIT)
Copyright (c) 2013 Michael Yoshitaka Erlewine
See readme for license block
"""

import unittest, sys
# todo: import doctest

runner = unittest.TextTestRunner(verbosity=1 + sys.argv.count('-v'))
suite = unittest.TestLoader().discover('tests')
runner.run(suite)
