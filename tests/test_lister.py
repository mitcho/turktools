# coding: utf-8
from unittest import TestCase
import lister

class TestLister(TestCase):
	def test_items_file(self):
		items = lister.graceful_read_items( 'tests/test_lister_items-1.txt' )
		self.assertEqual(len(items), 2)
		
		self.assertEqual(items[0].number, 1)
		self.assertEqual(items[0].section, 'test')
		self.assertEqual(items[0].condition, 'test condition')
		self.assertEqual(len(items[0].fields()), 1)

		self.assertEqual(items[1].number, 2)
		self.assertEqual(items[1].section, 'test')
		self.assertEqual(items[1].condition, 'another test condition')
		self.assertEqual(len(items[1].fields()), 2)

	def test_items_file_whitespace(self):
		items = lister.graceful_read_items( 'tests/test_lister_items-2.txt' )
		self.assertEqual(len(items), 1)
		
		self.assertEqual(items[0].number, 1)
		self.assertEqual(items[0].section, 'test')
		self.assertEqual(items[0].condition, 'test condition')

		# here is the tricky part: the item has three lines, the second of which
		# is blank. need to make sure this comes out as three fields.
		self.assertEqual(len(items[0].fields()), 3)

		# make sure we preserve whitespace, except for the line ending:
		self.assertEqual(items[0].fields(0), u'  aaa  ')
		
		# second field should be blank
		self.assertEqual(len(items[0].fields(1)), 0)
		
		# make sure we preserve whitespace, except for the line ending:
		self.assertEqual(items[0].fields(2), u'\tccc\t')
		