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

# Create a sample experiment, based on an array with specifications of the "shape" of
# sections. In the simplest case, item_specs can be an array of ints, which correspond
# to item counts in each section. Alternatively, they can be dicts of the form:
#   { items: ..., fields: ..., conditions: ... } // each of these being ints
def sample_experiment(item_specs):
	item_list = []
	for i in range(len(item_specs)):
		# the section specification could be a number or a dict
		spec = item_specs[i]
		if type(spec) is not dict:
			spec = {}
			spec.update(items = int(item_specs[i]))
		spec.setdefault('fields', 1)
		spec.setdefault('conditions', 1)

		for j in range(spec.get('items')):
			if spec.get('conditions') > 1:
				for k in range(spec.get('conditions')):
					item_list.append(lister.Item('section' + str(i), j, 'condition' + str(k), ['test'] * spec.get('fields')))
			else:
				item_list.append(lister.Item('section' + str(i), j, 'condition', ['test'] * spec.get('fields')))
	return lister.Experiment(item_list)

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
		exp = sample_experiment([dict(items=10, fields=1, conditions=1), dict(items=1, fields=2, conditions=1)])
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

class TestListerLists(TestCase):
	def test_lists(self):		
		exp = sample_experiment([10,11])
		exp.filler_sections = ['section0']
		self.assertEqual(exp.filler_sections, ['section0'])
		self.assertTrue(exp.has_fillers)

		self.assertEqual(exp.between_fillers, 0)
		self.assertEqual(exp.edge_fillers, 0)
		self.assertEqual(exp.max_between_fillers, 1)
		self.assertEqual(exp.max_edge_fillers, 5)
		
		list = exp.list(0, shuffle=False)
		other_list = list
		self.assertEqual(len(list), 10 + 11)
		# make sure that we can get a different result:
		while list == other_list:
			other_list = exp.list(0, shuffle=False)


		# change the filler settings
		# put one filler in between targets; no fillers left
		exp.between_fillers = 1
		self.assertEqual(exp.between_fillers, 1)
		self.assertEqual(exp.edge_fillers, 0)
		self.assertEqual(exp.max_between_fillers, 1)
		self.assertEqual(exp.max_edge_fillers, 0)

		# this has to be the same:
		list = exp.list(0, shuffle=False)
		other_list = exp.list(0, shuffle=False)
		self.assertEqual(len(list), 10 + 11)
		self.assertEqual(list, other_list)
		for i in range(1,20,2):
			self.assertEqual(list[i].section, 'section0')
		for i in range(0,21,2):
			self.assertEqual(list[i].section, 'section1')
		
		
		# change the filler settings:
		# push all the fillers to the edges
		exp.between_fillers = 0
		exp.edge_fillers = 5
		self.assertEqual(exp.between_fillers, 0)
		self.assertEqual(exp.edge_fillers, 5)
		self.assertEqual(exp.max_between_fillers, 1)
		self.assertEqual(exp.max_edge_fillers, 5)

		# this has to be the same:
		list = exp.list(0, shuffle=False)
		other_list = exp.list(0, shuffle=False)
		self.assertEqual(len(list), 10 + 11)
		self.assertEqual(list, other_list)
		for i in range(5):
			self.assertEqual(list[i].section, 'section0')
		for i in range(5):
			self.assertEqual(list[-i].section, 'section0')
		
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
