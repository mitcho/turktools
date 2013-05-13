# coding: utf-8
from unittest import TestCase
import decoder

class TestDecoder(TestCase):
	def test_math(self):
		self.assertEqual(2 + 2, 4)
	
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
	
	