# coding: utf-8
"""
Turk Lister
mitcho (Michael Yoshitaka Erlewine), mitcho@mitcho.com, May 2013

Takes an items file and produces a Turk items CSV file and a decode CSV file.

See the documentation for information on the input format. (It is based
on Gibson et al's Turkolizer, which in turn is based on Linger. However,
these formats are not exactly identical.)

This script is a clean-room rewrite of Gibson et al's Turkolizer, whose
copyright and licensing terms are unclear.

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

def graceful_write_csv(filename, data):
	from csv import DictWriter

	with open(filename, 'wb') as f:
		keys = data[0].keys()
		keys.sort()
		# be smarter about key sort?
		writer = DictWriter(f, keys, extrasaction = 'ignore')
		writer.writeheader()
		for row in data:
			writer.writerow(row)	

class Item:
	def __init__(self, section, number, condition):
		self.section = section
		self.number = int(number)
		self.condition = condition
		self.__fields = []

	def __repr__(self):
		return "[Item {0.section} {0.number} {0.condition} ({1})]".format(self, len(self.fields()))

	def fields(self, i = -1):
		if i != -1:
			if i < len(self.__fields):
				return self.__fields[i]
			else:
				return ''
		
		# strip off empty lines at the end of the fields:
		return_fields = self.__fields
		while len(return_fields) > 0 and return_fields[len(return_fields) - 1] == '':
			return_fields.pop()
		
		return return_fields

	def append_field(self, field):
		self.__fields.append(field)

class Section:
	def __init__(self, section_name, items):
		self.name = section_name
		self.__items = items

		# todo: add checks for section_name

		item_numbers = [t.number for t in self.items()]
		condition_names = []
		condition_names_set = set() # just a hack for getting the uniques as arrays are not hashable
		for num in item_numbers:
			conds = [i.condition for i in items if i.number == num]
			conds.sort()
			if conds not in condition_names:
				condition_names.append(conds)
		condition_counts = set([len(conds) for conds in condition_names])

		if len(condition_counts) > 1:
			print("ERROR: all item sets in a section must have the same number of conditions.")
			print("Some item sets in section {0} have".format(section_name), ', some have '.join(condition_counts))
			graceful_exit()

		self.condition_count = max(condition_counts)
		self.condition_names = condition_names
		
		self.item_count = len([t.number for t in items])
		self.item_set_count = len(set([t.number for t in items]))
	
	def __repr__(self):
		return "[Section {0.name}]".format(self)
	
	def items(self):
		return self.__items
	
	def verify(self):
		# numbers should start with 1 and increase sequentially
		item_numbers = [t.number for t in self.items()]
		item_count = len(item_numbers)
# 		print(item_numbers)
# 		for i in range(1, item_count + 1):
# 			# todo: do something with this assertion
# 			assert i in item_numbers
		# todo: each item has to have the same conditions

	def report(self):
		print('Section name:', self.name)
		print('Item sets:   ', self.item_set_count)
 		print('Conditions:  ', self.condition_count)
		for cond_set in self.condition_names:
	 		print('  ', ', '.join(cond_set))
 		
		print()

class Experiment:
	def __init__(self, items):
		self.__items = items
		self.__sections = {}
		for section in self.sections():
			section_items = [t for t in self.__items if t.section == section]
			self.__sections[section] = Section(section, section_items)
	
	def __repr__(self):
		return "[Experiment]"
	
	def field_counts(self):
		# return a list of tuples (field count, number of items with that count)
		field_counts = [len(i.fields()) for i in self.__items]
		count = field_counts.count
		result = [(ct, count(ct)) for ct in set(field_counts)]
		result.sort()
		return result

	def field_count(self):
		return max(self.field_counts())[0]
		
	def items_by_field_count(self, count):
		return [i for i in self.__items if len(i.fields()) == count]
	
	def item_count(self):
		return len(self.__items)
	
	def sections(self):
		return list(set([t.section for t in self.__items]))

	def verify(self):
		# todo: iterate better
		for section_name in self.sections():
			self.section(section_name).verify()

	def section(self, section_name):
		return self.__sections[section_name]

def graceful_read_items(filename):
	f = open(filename, 'rU')

	items = []
	
	# header lines must have: ^# section number condition$
	header_pattern = re.compile(r'^#\s+(\S+)\s+(\d+)\s+(.*?)\s*$')
	
	current_item = False
	for line in f.readlines():
		line = unicode(line, 'utf8')
		# strip off line endings:
		line = line.rstrip(u'\r\n')
		
		matched = header_pattern.match(line)
		
		if matched is False and current_item is False:
			# skip these lines. todo: print an error?
			print('weird')
			continue
		
		if matched:
			section, number, condition = matched.groups()
			# print(section, number, condition)
			current_item = Item(section, number, condition)
			items.append(current_item)
		else:
			current_item.append_field(line)
	
	return items

def main(items_file, lists):
	items = graceful_read_items(items_file)
	experiment = Experiment(items)
	experiment.verify()
	
	# print experiment details:
	print('-' * 20)
	for section_name in experiment.sections():
		experiment.section(section_name).report()
	
	item_count = experiment.item_count()
	
	fc = experiment.field_counts()
	if len(fc) == 1:
		print('Field count:', experiment.field_count())
	else:
		print('Maximum field count:', experiment.field_count())
		for (ct, items) in experiment.field_counts():
			if items > 1:
				print("  - {0} items with {1} field{2}"
					.format(items, ct, 's' if ct > 1 else ''))
			else:
				culprit = experiment.items_by_field_count(ct)
				print("  - 1 item with {1} field{2}: {3.section} {3.number} {3.condition}"
					.format(items, ct, 's' if ct > 1 else '', culprit[0]))
			if items < item_count * 0.1:
				print("    Is that an error?")
	
	print('-' * 20)

	name_part, extension = splitext(items_file)

if __name__ == '__main__':
	from os.path import splitext
	from sys import argv

	items_file = argv[1] if len(argv) > 1 else raw_input("Please enter the items file name: ")
	lists = argv[2] if len(argv) > 2 else raw_input("How many lists would you like to create: ")

	# todo: other parameters later?
	main(items_file, lists)
