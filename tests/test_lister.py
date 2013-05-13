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
		self.assertEqual(len(items[0].fields), 1)

		self.assertEqual(items[1].number, 2)
		self.assertEqual(items[1].section, 'test')
		self.assertEqual(items[1].condition, 'another test condition')
		self.assertEqual(len(items[1].fields), 2)

