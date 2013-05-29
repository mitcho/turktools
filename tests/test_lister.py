# coding: utf-8
from unittest import TestCase
import lister
import sys

class Silence:
	def __init__(self):
		self.__log = []
		return
	def __call__(self):
		return self.__log
	def write(self, x):
		self.__log.append(x)
		return

class TestLister(TestCase):
	def test_items_file(self):
		items = lister.graceful_read_items( 'tests/test_lister_items-1.txt' )
		self.assertEqual(len(items), 2)
		
		self.assertEqual(items[0].number, 1)
		self.assertEqual(items[0].section, 'test')
		self.assertEqual(items[0].condition_name, 'test condition')
		self.assertEqual(len(items[0].fields()), 1)

		self.assertEqual(items[1].number, 2)
		self.assertEqual(items[1].section, 'test')
		self.assertEqual(items[1].condition_name, 'another test condition')
		self.assertEqual(len(items[1].fields()), 2)

	def test_items_file_whitespace(self):
		items = lister.graceful_read_items( 'tests/test_lister_items-2.txt' )
		self.assertEqual(len(items), 1)
		
		self.assertEqual(items[0].number, 1)
		self.assertEqual(items[0].section, 'test')
		self.assertEqual(items[0].condition_name, 'test condition')

		# here is the tricky part: the item has three lines, the second of which
		# is blank. need to make sure this comes out as three fields.
		self.assertEqual(len(items[0].fields()), 3)

		# make sure we preserve whitespace, except for the line ending:
		self.assertEqual(items[0].field(0), u'  aaa  ')
		
		# second field should be blank
		self.assertEqual(len(items[0].field(1)), 0)
		
		# make sure we preserve whitespace, except for the line ending:
		self.assertEqual(items[0].field(2), u'\tccc\t')

class TestListerDifferentConditionNames(TestCase):
	def test_lister_different_condition_names(self):
		items = lister.graceful_read_items( 'tests/test_lister_items-3.txt' )
		self.assertEqual(len(items), 4)
		
		exp = lister.Experiment(items)
		self.assertEqual(len(exp.section_names), 1)
		self.assertEqual(exp.section_names[0], 'filler')
		sec = exp.section('filler')
		
		# two conditions at a time
		self.assertEqual(sec.condition_count, 2)
		cnames = sec.condition_sets
		# two different sets of condition names
		self.assertEqual(len(cnames), 2)
		# four actual distinct conditions
		self.assertEqual(len([cond for set in cnames for cond in set]), 4)

		excepted = False
		try:
			exp.verify()
		except SystemExit:
			excepted = True
		self.assertFalse(excepted)
	
	def test_lister_mismatch_condition_counts(self):
		items = lister.graceful_read_items( 'tests/test_lister_items-4.txt' )
		self.assertEqual(len(items), 5)
		
		exp = lister.Experiment(items)
		self.assertEqual(len(exp.section_names), 1)
		self.assertEqual(exp.section_names[0], 'filler')
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
		
class TestListerLatinSquareLists(TestCase):
	def test_lister_trivial_latin_square_lists(self):
		items = lister.graceful_read_items( 'tests/test_lister_items-1.txt' )
		self.assertEqual(len(items), 2)

		exp = lister.Experiment(items)
		self.assertEqual(len(exp.section_names), 1)
		self.assertEqual(exp.section_names[0], 'test')
		sec = exp.section('test')

		list0 = sec.latin_square_list(0)
		self.assertEqual(len(list0), 2)
		list1 = sec.latin_square_list(1)
		self.assertEqual(len(list1), 2)
		self.assertEqual(list0, list1)
	
	def test_lister_latin_square_lists(self):
		items = lister.graceful_read_items( 'tests/test_lister_items-3.txt' )
		self.assertEqual(len(items), 4)
		
		exp = lister.Experiment(items)
		self.assertEqual(len(exp.section_names), 1)
		self.assertEqual(exp.section_names[0], 'filler')
		sec = exp.section('filler')
		
		list0 = sec.latin_square_list(0)
		self.assertEqual(len(list0), 2)
		list1 = sec.latin_square_list(1)
		self.assertEqual(len(list1), 2)
		list2 = sec.latin_square_list(2)
		self.assertEqual(len(list2), 2)
		
		self.assertEqual(list0, list2)
		self.assertNotEqual(list0, list1)

class TestListerExperiments(TestCase):
	def test_items_experiments_basic(self):
		items = lister.graceful_read_items( 'tests/test_lister_items-1.txt' )
		exp = lister.Experiment(items)
		self.assertEqual(exp.field_count, 2)
		self.assertEqual(set(exp.field_count_counts), set([(2,1), (1,1)]))
		self.assertEqual(exp.items_by_field_count(1), [items[0]])
		self.assertEqual(exp.items_by_field_count(2), [items[1]])

		self.assertFalse(exp.has_fillers)
		self.assertEqual(exp.target_count, 2)
		self.assertEqual(exp.filler_count, 0)

	def test_items_experiments_only_filler(self):
		items = lister.graceful_read_items( 'tests/test_lister_items-3.txt' )
		exp = lister.Experiment(items)
		self.assertEqual(exp.field_count, 1)
		self.assertEqual(set(exp.field_count_counts), set([(1,4)]))
		self.assertEqual(set(exp.items_by_field_count(1)), set(items))

		silence = Silence()
		sys.stdout = silence

		exp.filler_sections = ['filler']
		# there's only one section, so...
		self.assertEqual(exp.filler_sections, [])
		self.assertFalse(exp.has_fillers)
		self.assertEqual(exp.target_count, 2)
		self.assertEqual(exp.filler_count, 0)

		exp.filler_sections = ['target']
		# now nothing's a filler, so...
		self.assertEqual(exp.filler_sections, [])
		self.assertFalse(exp.has_fillers)
		self.assertEqual(exp.target_count, 2)
		self.assertEqual(exp.filler_count, 0)
		sys.stdout = sys.__stdout__
		
		# let's make sure that the field_count_report() doesn't give us a warning
		silence = Silence()
		sys.stdout = silence
		exp.field_count_report()
		sys.stdout = sys.__stdout__
		found_warning = False
		for line in silence():
			if line.find('WARNING') > -1:
				found_warning = True
		self.assertFalse(found_warning)

	def test_items_experiments_field_count_warning(self):
		# construct items with 10 @ 1 + 1 @ 2
		items = []
		items.append(lister.Item('test', 1, 'test', ['test', 'extra!']))
		for i in range(10):
			items.append(lister.Item('test', i + 2, 'test', ['test']))

		exp = lister.Experiment(items)
		self.assertEqual(exp.field_count, 2)
		self.assertEqual(set(exp.field_count_counts), set([(2,1), (1,10)]))
		self.assertEqual(len(exp.items_by_field_count(1)), 10)
		self.assertEqual(len(exp.items_by_field_count(2)), 1)

		# let's make sure that the field_count_report() tells us something's off.
		silence = Silence()
		sys.stdout = silence
		exp.field_count_report()
		sys.stdout = sys.__stdout__
		found_warning = False
		for line in silence():
			if line.find('WARNING') > -1:
				found_warning = True
		self.assertTrue(found_warning)

class TestListerUtilities(TestCase):
	def test_get_in_range(self):
		silence = Silence()
		sys.stdout = silence

		# we can't test the raw_input part of get_in_range
		# but we can test the automated part.
		self.assertEqual(lister.get_in_range(5, 'test', -1), 0)
		self.assertEqual(lister.get_in_range(5, 'test', 0), 0)
		self.assertEqual(lister.get_in_range(5, 'test', 1), 1)
		self.assertEqual(lister.get_in_range(5, 'test', 5), 5)
		self.assertEqual(lister.get_in_range(5, 'test', 6), 5)
		
		sys.stdout = sys.__stdout__

	def test_multinomial(self):
		def test_multinomial_function(holes, pigeons):
			hit = lister.multinomial(holes, pigeons)
			self.assertEqual(len(hit), holes)
			self.assertEqual(sum(hit), pigeons)
			self.assertTrue(min(hit) >= 0)
			
			if holes > 1:
				# make sure the result isn't deterministic:
				hit2 = []
				while hit == hit2:
					hit2 = lister.multinomial(holes, pigeons)
				self.assertNotEqual(hit, hit2)
			else:
				hit2 = lister.multinomial(holes, pigeons)
				self.assertEqual(hit, hit2)
		
		test_multinomial_function(5,2)
		test_multinomial_function(10,20)
		test_multinomial_function(1,20)
