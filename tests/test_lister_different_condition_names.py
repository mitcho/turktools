# coding: utf-8
from unittest import TestCase
import lister
import sys

class Silence:
	def __init__(self):
		return
	def __call__(self):
		return
	def write(self, x):
		return

class TestListerDifferentConditionNames(TestCase):
	def test_lister_different_condition_names(self):
		items = lister.graceful_read_items( 'tests/test_lister_different_condition_names-1.txt' )
		self.assertEqual(len(items), 4)
		
		exp = lister.Experiment(items)
		self.assertEqual(len(exp.sections()), 1)
		self.assertEqual(exp.sections()[0], 'filler')
		sec = exp.section('filler')
		
		# two conditions at a time
		self.assertEqual(sec.condition_count, 2)
		cnames = sec.condition_sets
		# two different sets of condition names
		self.assertEqual(len(cnames), 2)
		# four actual distinct conditions
		self.assertEqual(len([cond for set in cnames for cond in set]), 4)

		exp.verify()
	
	def test_lister_mismatch_condition_counts(self):
		items = lister.graceful_read_items( 'tests/test_lister_different_condition_names-2.txt' )
		self.assertEqual(len(items), 5)
		
		exp = lister.Experiment(items)
		self.assertEqual(len(exp.sections()), 1)
		self.assertEqual(exp.sections()[0], 'filler')
		sec = exp.section('filler')
		
		# condition count is three
		self.assertEqual(sec.condition_count, 3)
		cnames = sec.condition_sets
		# two different sets of condition names
		self.assertEqual(len(cnames), 2)
		# five actual distinct conditions
		self.assertEqual(len([cond for set in cnames for cond in set]), 5)

		silence = Silence()
		sys.stdout = silence
		
		excepted = False
		try:
			exp.verify()
		except SystemExit:
			excepted = True

		self.assertTrue(excepted)

		sys.stdout = sys.__stdout__
		