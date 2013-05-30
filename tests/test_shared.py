# coding: utf-8
from unittest import TestCase
import sys
import decoder, lister, templater, simulator

class Silence:
	def __init__(self):
		self.__log = []
		return
	def __call__(self):
		return self.__log
	def write(self, x):
		self.__log.append(x)
		return

class TestCSV(TestCase):
	def run_numeric_test(self, write_module, read_module):
		data = [
			{'a':1,'b':2,'c':3},
			{'a':4,'b':5,'c':6},
			{'a':7,'b':8,'c':9},
		]
		# note that lister doesn't have a graceful_read_csv, so still use decoder for that
		write_module.graceful_write_csv( 'tests/tmp_test_numeric_csv.csv', data )
		read_data = read_module.graceful_read_csv( 'tests/tmp_test_numeric_csv.csv' )
		self.assertNotEqual(data, read_data)
	
	def run_text_test(self, write_module, read_module):
		data = [
			{'a':'1','b':'2','c':'3'},
			{'a':'4','b':'5','c':'6'},
			{'a':'7','b':'8','c':'9'},
		]
		# note that lister doesn't have a graceful_read_csv, so still use decoder for that
		write_module.graceful_write_csv( 'tests/tmp_test_text_csv.csv', data )
		read_data = read_module.graceful_read_csv( 'tests/tmp_test_text_csv.csv' )
		self.assertEqual(data, read_data)
	
	def test_csv(self):
		# modules which define graceful_read_csv:
		writes = [decoder, lister]
		reads = [decoder, simulator]
	
		for write in writes:
			for read in reads:
				self.run_numeric_test(write, read)
				self.run_text_test(write, read)
	
expected = """# filler 1 hello
Hello

# filler 1 goodbye
Goodbye

# filler 2 welcome
Welcome

# filler 2 goaway
Go away

# filler 2 extra
Extra!
"""

class TestRead(TestCase):
	def test_graceful_read(self):
		for module in [simulator, templater]:
			text = module.graceful_read('tests/test_lister_items-4.txt')
			self.assertEqual(text, expected)
			text = module.graceful_read('tests/test_lister_items-4.txt')
			self.assertEqual(text, expected)

			silence = Silence()
			sys.stdout = silence
			
			exited = False
			try:
				module.graceful_read('tests/does_not_exist.txt')
			except SystemExit:
				exited = True
			self.assertTrue(exited)

			sys.stdout = sys.__stdout__