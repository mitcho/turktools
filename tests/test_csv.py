# coding: utf-8
from unittest import TestCase
import decoder, lister

class TestCSV(TestCase):
	def test_numeric_csv(self):
		data = [
			{'a':1,'b':2,'c':3},
			{'a':4,'b':5,'c':6},
			{'a':7,'b':8,'c':9},
		]
		decoder.graceful_write_csv( 'tests/tmp_test_numeric_csv.csv', data )
		read_data = decoder.graceful_read_csv( 'tests/tmp_test_numeric_csv.csv' )
		self.assertNotEqual(data, read_data)
		
	def test_text_csv(self):
		data = [
			{'a':'1','b':'2','c':'3'},
			{'a':'4','b':'5','c':'6'},
			{'a':'7','b':'8','c':'9'},
		]
		decoder.graceful_write_csv( 'tests/tmp_test_text_csv.csv', data )
		read_data = decoder.graceful_read_csv( 'tests/tmp_test_text_csv.csv' )
		self.assertEqual(data, read_data)
	
	# do that again, but now use lister.graceful_write_csv.
	# note that lister doesn't have a graceful_read_csv, so still use decoder for that
	def test_numeric_csv_lister(self):
		data = [
			{'a':1,'b':2,'c':3},
			{'a':4,'b':5,'c':6},
			{'a':7,'b':8,'c':9},
		]
		lister.graceful_write_csv( 'tests/tmp_test_numeric_csv.csv', data )
		read_data = decoder.graceful_read_csv( 'tests/tmp_test_numeric_csv.csv' )
		self.assertNotEqual(data, read_data)
		
	def test_text_csv_lister(self):
		data = [
			{'a':'1','b':'2','c':'3'},
			{'a':'4','b':'5','c':'6'},
			{'a':'7','b':'8','c':'9'},
		]
		lister.graceful_write_csv( 'tests/tmp_test_text_csv.csv', data )
		read_data = decoder.graceful_read_csv( 'tests/tmp_test_text_csv.csv' )
		self.assertEqual(data, read_data)
	
