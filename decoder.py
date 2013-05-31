# coding: utf-8
"""
turktools decoder
mitcho (Michael Yoshitaka Erlewine), mitcho@mitcho.com, April 2013

Decode a Turk results file into a format optimized for analysis

The MIT License (MIT)
Copyright (c) 2013 Michael Yoshitaka Erlewine

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from __future__ import print_function
import re, atexit

@atexit.register
def graceful_exit():
	from platform import system
	if system() == 'Windows':
		raw_input('Press enter to close the window...')

# add tab completion to raw_input, for those platforms that support it
try:
	import readline
	if 'libedit' in readline.__doc__:
		readline.parse_and_bind("bind ^I rl_complete")
	else:
		readline.parse_and_bind("tab: complete")
except ImportError:
	pass

def graceful_read_csv(filename):
	from csv import DictReader

	data = []
	try:
		f = open(filename, 'rb')
	except IOError as e:
		print( "ERROR:", e.strerror )
		exit()

	csvreader = DictReader(f)
	while True:
		try: row = csvreader.next()
		except: break
		data.append(row)

	return data

def graceful_write_csv(filename, data, keys = False):
	from csv import DictWriter

	if keys is False:
		keys = data[0].keys()
		# be smarter about key sort?
		keys.sort()

	with open(filename, 'wb') as f:
		# setting keys here fixes the order of columns
		writer = DictWriter(f, keys, extrasaction = 'ignore')

		# use this cumbersome line instead of writeheader() for python 2.6 compat:
		writer.writerow(dict(zip(keys, keys)))
		for row in data:
			writer.writerow(row)

class ResultsData(object):
	__data = []

	def __init__(self, data = False, file = False):
		if data is not False:
			self.__data = data
		if file is not False:
			self.readfile(file)

	@property
	def data(self):
		return self.__data

	def readfile(self, filename):
		self.__data = graceful_read_csv(filename)

	def verify(self):
		if len(self.data) == 0:
			print( "ERROR: It looks like this results file is missing data or is not formatted correctly (no data found). Please try again." )
			exit()

		for expected in ['Title', 'Description', 'Keywords', 'Reward']:
			if expected not in self.data[0]:
				print( "ERROR: It looks like the results file is not formatted correctly (missing expected column {0}). Please try again.".format(expected) )
				exit()
		
		if 'Input.field_1_1' not in self.data[0] and 'Input.trial_1_1' in self.data[0]:
			print( "ERROR: This results file is based on an older version of turktools, which probably gave you a decode file." )
			print( "In that case, please use the old decoder, available at https://github.com/mitcho/turktools/tree/old-decoder ." )
			exit()

		if 'Input.field_1_1' not in self.data[0] or 'Input.item_1_section' not in self.data[0]:
			print( "ERROR: This results file looks like it was not constructed with turktools, or there was a problem reading the results file." )
			exit()

		item_numbers = self.item_numbers
		if len(item_numbers) == 0 or \
			min(item_numbers) != 1 or \
			max(item_numbers) != len(item_numbers):
			print( "ERROR: It looks like this results file is missing data or is not formatted correctly (display item numbers could not be read). Please try again." )
			exit()

	def report(self):
		print( '-' * 20 )
		print( 'Title:       ', self.data[0]['Title'] )
		print( 'Description: ', self.data[0]['Description'] )
		print( 'Keywords:    ', self.data[0]['Keywords'] )
		print( 'Reward:      ', self.data[0]['Reward'] )
		print( '-' * 20 )

	@property
	def item_numbers(self):
		# todo: is there a better way to get the item_numbers and check it?
		keys = self.data[0].keys()
		re_item_section = re.compile(r'^Input.item_(\d+)_section$')
		numbers = [int(re_item_section.sub('\\1', key)) for key in keys if re_item_section.match(key)]
		numbers.sort()
		return numbers

	@property
	def condition_names(self):
		conditions = []
		keys = self.data[0].keys()
		for key in keys:
			if re.match(r'^Input\.item_(\d+)_condition$', key):
				conditions = conditions + [row[key] for row in self.data]
		return list(set(conditions))

	@property
	def factor_count(self):
		return 1 + max([condition.count('-') for condition in self.condition_names])

	def decode_map(self, row):
		results = {}
		fc = self.factor_count
		for n in self.item_numbers:
			results[n] = [
				('PresentationOrder', n),
				('Section', row['Input.item_{0}_section'.format(n)]),
				('Item', int(row['Input.item_{0}_number'.format(n)])),
				('Condition', row['Input.item_{0}_condition'.format(n)]),
			]
			
			factors = row['Input.item_{0}_condition'.format(n)].split('-')
			
			for i in range(fc):
				column = 'Factor{0}'.format(i + 1)
				value = factors[i] if i < len(factors) else ''
				results[n].append((column, value))
		return results

	def assignment_data(self, row):
		# copy user/assignment meta
		data = [
			('WorkerId', row['WorkerId']),
			('AssignmentId', row['AssignmentId']),
			('AssignmentStatus', row['AssignmentStatus']),
			('WorkTimeInSeconds', row['WorkTimeInSeconds']),
			('List', row['Input.list']),
		]
		return data

	def decode(self):
		decoded_data = []

		re_extra = re.compile('^Answer\.(\D+)$');
		for row in self.data:
			decode_map = self.decode_map(row)
			row_meta = self.assignment_data(row)

			for n in self.item_numbers:
				re_input = re.compile(r'^Input\.field_{0}_(\d+)$'.format(n));
				re_answer = re.compile(r'^Answer\.(.*?\D)_?{0}$'.format(n));
				re_sample = re.compile(r'^Answer\.(.*?\D)_?Sample{0}$'.format(n));
			
				# this line does the merge:
				data = row_meta[:]
				data = data + decode_map[n][:]
				fields = []
				answers = []
				extras = []
				
				for field in row.keys():
					if re_input.match(field) is not None:
						fields.append((re_input.sub('field_\\1', field), row[field]))
						continue
					
					if re_answer.match(field) is not None and re_sample.match(field) is None:
						answers.append((re_answer.sub('\\1', field), row[field]))
						continue
					
					if re_extra.match(field) is not None:
						extras.append((re_extra.sub('\\1', field), row[field]))
				
				data = data + fields + answers + extras
				# todo: check that each row/item has the same number of fields!

				# todo: get sample/practice item answers?
				decoded_data.append(data)
		return decoded_data

def main(filename):
	
	results = ResultsData(file = filename)
	results.verify()
	results.report()
	decoded_data = results.decode()

	from os.path import splitext
	name_part, extension = splitext(filename)
	decoded_filename = name_part + '.decoded.csv'
	
	data_dict = [dict(row) for row in decoded_data]
	decoded_keys = [entry[0] for entry in decoded_data[0]]
	graceful_write_csv(decoded_filename, data_dict, keys = decoded_keys)

	print( 'Successfully wrote decoded results to ' + decoded_filename )

if __name__ == '__main__':
	from sys import argv

	filename = argv[1] if len(argv) > 1 else raw_input("Please enter the Turk results file name: ")

	main(filename)
