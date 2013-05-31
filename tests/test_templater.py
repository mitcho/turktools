# coding: utf-8
from unittest import TestCase
import templater
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

class TestFakeMustaches(TestCase):
	def test_fake_mustaches(self):
		FM = templater.FakeMustaches
		self.assertEqual(FM(' {{test}} {{rar}} ').safe_substitute(test='rar', rar='test'),
			' rar test ')
		self.assertEqual(FM(' {{test}} {{rar}} ').substitute(test='rar', rar='test'),
			' rar test ')
		self.assertEqual(FM(' {test} {{rar}} ').substitute(test='rar', rar='test'),
			' {test} test ')
				
		excepted = False
		try:
			FM(' {{test}} {{rar}} ').substitute(test='rar')
		except KeyError:
			excepted = True
		self.assertTrue(excepted)

		excepted = False
		try:
			FM(' {{test}} {{rar}} ').safe_substitute(test='rar')
		except KeyError:
			excepted = True
		self.assertFalse(excepted)

class TestTemplater(TestCase):
	def run_templater_main(self, file_prefix):
		silence = Silence()
		sys.stdout = silence
	
		filename = file_prefix + '.txt'
	
		excepted = False
		try:
			template_string = templater.graceful_read(filename)
		except SystemExit:
			excepted = True
		self.assertFalse(excepted)

		exited = False
		try:
			templater.main(filename, template_string, 10, 'test')
		except SystemExit:
			exited = True
		# self.assertTrue(exited)

		sys.stdout = sys.__stdout__

		excepted = False
		try:
			output = templater.graceful_read(file_prefix + '-test-10.txt')
		except SystemExit:
			excepted = True
		self.assertFalse(excepted)
		
		self.assertTrue(len(output) > 0)

		# return the result and the print log
		return (output, silence())

	def test_file(self):
		silence = Silence()
		sys.stdout = silence
		
		excepted = False
		try:
			templater.graceful_read('/var/null')
		except SystemExit:
			excepted = True
		self.assertTrue(excepted)

		sys.stdout = sys.__stdout__

	def test_template1(self):
		import re
		output, log = self.run_templater_main('tests/test_templater_template-1')

		self.assertFalse(re.match(r'success', '\n'.join(log), re.IGNORECASE) is None)
		# print(output, type(output))
		self.assertTrue(output.find('{{') == -1)
		self.assertTrue(re.search(r'\{\{.*\}\}', output) is None)
		self.assertFalse(re.search(r'^Code: test\r?\n?$', output, re.MULTILINE) is None)
		self.assertFalse(re.search(r'^Number: 10\r?\n?$', output, re.MULTILINE) is None)
	def test_template2(self):
		import re
		output, log = self.run_templater_main('tests/test_templater_template-2')

		self.assertFalse(re.match(r'success', '\n'.join(log), re.IGNORECASE) is None)
		self.assertTrue(output.find('{{') == -1)
		self.assertTrue(re.search(r'\{\{.*\}\}', output) is None)
		self.assertFalse(re.search(r'^Code: test\r?\n?$', output, re.MULTILINE) is None)
		self.assertFalse(re.search(r'^Total number: 10\r?\n?$', output, re.MULTILINE) is None)
		for i in range(1,11):
			self.assertFalse(re.search(r'^Code in item: test\r?\n?$', output, re.MULTILINE) is None)
			self.assertFalse(re.search(r'^Total number in item: 10\r?\n?$', output, re.MULTILINE) is None)
			self.assertFalse(re.search('^Item number: ' + str(i) + '\r?\n?$', output, re.MULTILINE) is None)
			self.assertFalse(re.search('^Field 1: \$\{field_' + str(i) + '_1\}\r?\n?$', output, re.MULTILINE) is None)
			self.assertFalse(re.search('^Field 2: \$\{field_' + str(i) + '_2\}\r?\n?$', output, re.MULTILINE) is None)
# 	@expectedFailure
# 	def test_template_nonsense(self):
# 		import re
# 		output, log = self.run_templater_main('tests/test_templater_template-1')
# 
# 		self.assertFalse(re.search(r'^Extra: \r?\n?$', output, re.MULTILINE) is None)
# 		self.assertTrue(output.find('nonsense') == -1)
# 
# 		output, log = self.run_templater_main('tests/test_templater_template-2')
# 
# 		self.assertFalse(re.search(r'^Extra: \r?\n?$', output, re.MULTILINE) is None)
# 		self.assertTrue(output.find('nonsense') == -1)
