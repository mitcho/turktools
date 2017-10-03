# coding: utf-8
"""
Turk Lister
Michael Yoshitaka ERLEWINE, mitcho@mitcho.com, May 2013

Takes an items file and produces a Turk items CSV file and a decode CSV file.

See the documentation for information on the input format. (It is based
on Gibson et al's Turkolizer, which in turn is based on Linger. However,
these formats are not exactly identical.)

This script is a clean-room rewrite of Gibson et al's Turkolizer, whose
copyright and licensing terms are unclear.

The MIT License (MIT)
Copyright (c) 2013--2017 Michael Yoshitaka ERLEWINE and contributors

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

def graceful_write_csv(filename, data, keys = False):
	import csv

	if keys is False:
		keys = data[0].keys()
		# be smarter about key sort?
		keys.sort()

	with open(filename, 'wb') as f:
		# setting keys here fixes the order of columns
		writer = csv.DictWriter(f, keys, extrasaction = 'ignore', quoting = csv.QUOTE_NONNUMERIC)

		# use this cumbersome line instead of writeheader() for python 2.6 compat:
		writer.writerow(dict(zip(keys, keys)))
		# encode utf8 on writerow, thanks to Anoop Sarkar:
		for row in data:
			writer.writerow(dict((k, v.encode('utf8') if type(v) is unicode else v) for k, v in row.items()))

def lcm(numbers):
	from fractions import gcd
	return reduce(lambda x, y: (x*y)/gcd(x,y), numbers, 1)

class Item(object):
	def __init__(self, section, number, condition_name, fields = False):
		self.section = section
		self.number = int(number)
		
		# the condition name is an actual text label
		self.condition_name = condition_name
		# the condition attribute will be an integer. it will be set later.
		# todo: maybe this should be created on init instead, somehow
		self.condition = False

		self.__fields = []
		if fields and type(fields) == list:
			self.__fields = fields

	def __repr__(self):
		return "[Item {0.section} {0.number} {0.condition_name} ({1})]".format(self, len(self.fields()))

	def field(self, i = 0):
		if i < len(self.__fields):
			return self.__fields[i]
		else:
			return ''
		
	def fields(self, number_of_fields = False):
		return_fields = self.__fields
		if number_of_fields is False:
			# strip off empty lines at the end of the fields:
			while len(return_fields) > 0 and return_fields[len(return_fields) - 1] == '':
				return_fields.pop()
			return return_fields
		
		return_fields = self.__fields[0:number_of_fields]
		if len(return_fields) < number_of_fields:
			return_fields = return_fields + [''] * (number_of_fields - len(return_fields))
		
		return return_fields

	def append_field(self, field):
		self.__fields.append(field)

class Section(object):
	def __init__(self, section_name, items):
		self.name = section_name
		self.__items = items

		# todo: add checks for section_name
		condition_sets = []
		self.__item_numbers = list(set([item.number for item in self.items]))
		for num in self.__item_numbers:
			item_set = [item for item in items if item.number == num]
			# sort item set by condition name:
			item_set.sort(key=lambda x: x.condition_name)
			# pick out the condition names to add to the condition_sets:
			conds = [item.condition_name for item in item_set]
			if conds not in condition_sets:
				condition_sets.append(conds)

			# set the condition number attribute on each item in the set:
			for i in range(len(conds)):
				item_set[i].condition = i

		condition_counts = set([len(conds) for conds in condition_sets])
		self.condition_count = max(condition_counts)
		self.condition_sets = condition_sets
	
	def __repr__(self):
		return "[Section {0.name}]".format(self)
	
	@property
	def items(self):
		return self.__items

	@property
	def item_count(self):
		return len(self.items())

	@property
	def item_set_count(self):
		return len(self.__item_numbers)
	
	# returns a single item, given an item number and condition number (not condition name!)
	def item(self, item_number, condition_number):
		matches = [item for item in self.items
			if item.number == item_number and item.condition == condition_number]

		# todo: do something about this assert
		assert len(matches) == 1
		
		return matches[0]
	
	def verify(self):
		# numbers should start with 1 and increase sequentially
		item_count = len(self.__item_numbers)
# 		print(self.__item_numbers)
# 		for i in range(1, item_count + 1):
# 			# todo: do something with this assertion
# 			assert i in self.__item_numbers

		condition_counts = set([str(len(conds)) for conds in self.condition_sets])
		if len(condition_counts) > 1:
			print("ERROR: all item sets in a section must have the same number of conditions.")
			print("Some item sets in section {0} have" . format(self.name), ', some have '.join(condition_counts))
			exit()
		
		for item in self.items:
			if item.condition is False:
				print("ERROR: {0} was not assigned a condition number".format(item))
				exit()

	def report(self):
		print('Section name:', self.name)
		print('Item sets:   ', self.item_set_count)
 		print('Conditions:  ', self.condition_count)
		for cond_set in self.condition_sets:
	 		print('  ', ', '.join(cond_set))
 		
		print()
	
	# offset is the list number, starting with 0 (though that doesn't actually matter much)
	def latin_square_list(self, offset):
		return [self.item(n, (n + offset) % self.condition_count) for n in self.__item_numbers]

class Experiment(object):
	def __init__(self, items):
		self.__original_items = items
		self.__section_names = list(set([item.section for item in items]))
		self.__sections = {}
		for section in self.section_names:
			section_items = [t for t in items if t.section == section]
			self.__sections[section] = Section(section, section_items)

		# filler settings:
		self.has_fillers = False
		self.__filler_sections = []
		self.between_fillers = 0
		self.edge_fillers = 0
	
	def __repr__(self):
		return "[Experiment]"
	
	@property
	def field_count_counts(self):
		# return a list of tuples (field count, number of items with that count)
		field_counts = [len(i.fields()) for i in self.items]
		count = field_counts.count
		result = [(ct, count(ct)) for ct in set(field_counts)]
		result.sort()
		return result

	@property
	def field_count(self):
		return max(self.field_count_counts)[0]
	
	@property
	def items(self):
		return [i for section in self.__sections.values() for i in section.items]
	
	def items_by_field_count(self, count):
		return [i for i in self.items if len(i.fields()) == count]
	
	@property
	def item_count(self):
		return len(self.items)
	
	@property
	def target_count(self):
		return sum([self.section(sec).item_set_count
			for sec in self.section_names if sec not in self.filler_sections])

	@property
	def filler_count(self):
		return sum([self.section(sec).item_set_count
			for sec in self.section_names if sec in self.filler_sections])
	
	@property
	def section_names(self):
		return self.__section_names

	@property
	def condition_counts(self):
		return [section.condition_count for section in self.__sections.values()]

	@property
	def list_number_multiplier(self):
		# the list number multiplier is the least-common-multiple of the
		# condition names across all sections.
		return lcm(self.condition_counts)
	
	def verify(self):
		# todo: iterate better
		for section_name in self.section_names:
			self.section(section_name).verify()

	def section(self, section_name):
		return self.__sections[section_name]

	def field_count_report(self):
		fcc = self.field_count_counts
		if len(fcc) == 1:
			print('Field count: ', self.field_count)
		else:
			print('Maximum field count:', self.field_count)
			for (ct, items) in fcc:
				if items > 1:
					print("  - {0} items with {1} field{2}"
						.format(items, ct, 's' if ct > 1 else ''))
				else:
					culprit = self.items_by_field_count(ct)
					print("  - 1 item with {1} field{2}: {3.section} {3.number} {3.condition_name}"
						.format(items, ct, 's' if ct > 1 else '', culprit[0]))
				if items < self.item_count * 0.1:
					print("WARNING: Is that an error?")

	@property
	def filler_sections(self):
		if self.has_fillers:
			return self.__filler_sections
		else:
			return []
	
	@filler_sections.setter
	def filler_sections(self, sections):
		self.__filler_sections = [section for section in sections if section in self.section_names]
		self.has_fillers = True
		if len(self.__filler_sections) == len(self.section_names):
			self.has_fillers = False
			print("WARNING: All your sections are designated as fillers!")
		if len(self.__filler_sections) == 0:
			self.has_fillers = False
			print("WARNING: You have no sections designated as fillers.")

	@property
	def max_between_fillers(self):
		from math import floor
		return int(floor(self.filler_count / (self.target_count - 1)))
	
	@property
	def max_edge_fillers(self):
		return int(round(
			(self.filler_count - (self.target_count - 1) * self.between_fillers)
			/ 2))
	
	# Without the shuffle option, items will not be randomized within their section's
	# latin square lists. This option exists for unit testing, in order to construct
	# deterministic tests.
	def list(self, list_number, shuffle=True):
		target_items = [item
			for sec in self.section_names if sec not in self.filler_sections
			for item in self.section(sec).latin_square_list(list_number)]
		filler_items = [item
			for sec in self.section_names if sec in self.filler_sections
			for item in self.section(sec).latin_square_list(list_number)]
		
		if shuffle:
			from random import shuffle
			shuffle(target_items)
			shuffle(filler_items)
		
		# Start with the target items
		list = target_items[:]
		
		if self.has_fillers:
			# In general, when placing fillers systematically, loop over targets and 
			# find that target in the current list. Mutate relative to that index.

			# First, place between_fillers fillers between the targets:
			if self.between_fillers > 0:
				for i in range(len(target_items) - 1):
					# place fillers after this target:
					target_target = target_items[i]
					target_index = list.index(target_target)
					for j in range(self.between_fillers):
						list.insert(target_index + 1, filler_items.pop())

			# Second, place edge_fillers fillers at the edges:
			if self.edge_fillers > 0:
				for j in range(self.edge_fillers):
					list.insert(0, filler_items.pop())
					list.insert(len(list), filler_items.pop())
			
			# Third, if there are remaining fillers, place them randomly
			# print('Remaining fillers:',len(filler_items))
			if len(filler_items) > 0:
				bins = len(target_items) + 1
				sample = multinomial(bins, len(filler_items))
				# print(bins, len(filler_items), sample)
				# sample[0] will be a special case:
				for j in range(sample[0]):
					list.insert(0, filler_items.pop())
				# for each other bin, find the corresponding target:
				for i in range(len(target_items)):
					# place fillers after this target:
					target_target = target_items[i]
					target_index = list.index(target_target)
					for j in range(sample[i + 1]):
						list.insert(target_index + 1, filler_items.pop())

			# no fillers should be left here:
			assert len(filler_items) == 0
					
		return list

	# list is a list of items
	# return fields in a list with (key, value) entries
	def fields_from_list(self, list):
		fields = []

		for i in range(len(list)):
			item = list[i]
			# the display order starts with 1:
			display_order = i + 1
			item_fields = item.fields(self.field_count)
			# add decode information:
			fields = fields + [
				('item_{0}_section'.format(display_order), item.section),
				('item_{0}_number'.format(display_order), item.number),
				('item_{0}_condition'.format(display_order), item.condition_name),
			]
			# add the fields:
			fields = fields + [ ('field_{0}_{1}'.format(display_order, j + 1), item_fields[j])
				for j in range(self.field_count) ]

		return fields

# placing pigeons into holes
def multinomial(holes, pigeons):
	from random import randrange
	sample = [randrange(holes) for i in range(pigeons)]
	return [sample.count(i) for i in range(holes)]

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
			section, number, condition_name = matched.groups()
			# print(section, number, condition_name)
			current_item = Item(section, number, condition_name)
			items.append(current_item)
		else:
			current_item.append_field(line)
	
	return items

def get_in_range(max, label, given=False):
	if given is not False:
		value = int(given)
		if value < 0:
			print("Specified {0} ({1}) could not be used."
				.format(label, value))
			print("Using 0 instead.")
			value = 0
		if value > max:
			print("Specified {0} ({1}) could not be used."
				.format(label, value))
			print("Using {0} instead.".format(max))
			value = max
	else:
		value = -1
		while value < 0 or value > max:
			raw = raw_input("Minimum {0} ([0]-{1}): ".format(label, max))

			if raw.isdigit() == False:
				print("Using the default value, 0.")
				value = 0
				continue
			
			value = int(raw)
			
			if value < 0 or value > max:
				print("Please try again.")
	return value

def main(args):
	from os.path import splitext
	
	items_file = args[0] if len(args) > 0 else raw_input("Please enter the items file name: ")
	items = graceful_read_items(items_file)
	experiment = Experiment(items)
	experiment.verify()
	
	# PRINT EXPERIMENT REPORT
	print('-' * 20)
	for section_name in experiment.section_names:
		experiment.section(section_name).report()
	experiment.field_count_report()
	print('-' * 20)
	# END EXPERIMENT REPORT

	# SET FILLER SECTIONS AND GUIDANCE
	filler_sections_string = args[1] if len(args) > 1 else raw_input("Enter filler section names, separated by commas: ")
	experiment.filler_sections = re.split(', *', filler_sections_string)

	if experiment.has_fillers:
		print('Filler section{0}:'.format('s' if len(experiment.filler_sections) > 1 else ''),
			', '.join(experiment.filler_sections))
		print('Each list will have {0.target_count} target items and {0.filler_count} filler items'
			.format(experiment))
		
		# set between_fillers
		if experiment.target_count > 1 and experiment.max_between_fillers > 0:
			experiment.between_fillers = get_in_range(
				experiment.max_between_fillers,
				'number of fillers between targets',
				args[2] if len(args) > 2 else False)

		if experiment.target_count > 1 and experiment.max_between_fillers == 0:
			print("WARNING: There are not enough fillers. There will be target items presented one after another.")

		# set edge_fillers
		if experiment.max_edge_fillers > 0:
			experiment.edge_fillers = get_in_range(
				experiment.max_edge_fillers,
				'number of fillers at the beginning and end of lists',
				args[3] if len(args) > 3 else False)
		else:
			experiment.edge_fillers = 0
	
	# END FILLER SETTINGS

	# SET THE NUMBER OF LISTS
	lnm = experiment.list_number_multiplier
	number_of_lists = args[4] if len(args) > 4 else raw_input("How many lists would you like to create (enter a multiple of {0}): ".format(lnm))
	
	if number_of_lists.isdigit():
		number_of_lists = int(number_of_lists)
	else:
		print("The value given, '{0}', could not be read. The minimum number, {1}, will be used instead."
			.format(number_of_lists, lnm))
		number_of_lists = lnm

	if number_of_lists < lnm:
		print("The minimum number, {0}, will be used instead.".format(lnm))
		number_of_lists = lnm
	if number_of_lists % lnm != 0:
		number_of_lists = int(round(number_of_lists / lnm, 0) * lnm)
		print("The multiple of {0}, {1}, will be used instead.".format(lnm, number_of_lists))
	# END THE NUMBER OF LISTS

	# ASK ABOUT REVERSE LISTS
	reverse = False
	want_reverse = args[5] if len(args) > 5 else raw_input("Would you like reverse lists? ([yes], no) ")
	if want_reverse == '' or want_reverse[0].lower() == 'y':
		reverse = True
	
	if reverse:
		print("Randomizing {0} lists and their reverses, for a total of {1} lists..."
			.format(number_of_lists, number_of_lists * 2))
	else:
		print("Randomizing {0} lists...".format(number_of_lists))
	# END REVERSE LISTS

	name_part, extension = splitext(items_file)
	data = []
	for list_number in range(number_of_lists):
		list = experiment.list(list_number)
		if reverse:
			entry = [('list', list_number * 2)] + experiment.fields_from_list(list)
			data.append(dict(entry))
			list.reverse()
			entry = [('list', list_number * 2 + 1)] + experiment.fields_from_list(list)
			data.append(dict(entry))
		else:
			entry = [('list', list_number)] + experiment.fields_from_list(list)
			data.append(dict(entry))

		# todo: make sure that all the lists generate the same keys
		keys = [entry[0] for entry in entry]

	graceful_write_csv(name_part + '.turk.csv', data, keys)
	print( 'Successfully wrote randomized lists to ' + name_part + '.turk.csv' )
	print( 'The associated template file should take {0} items.'
			.format(experiment.target_count + experiment.filler_count) )
	graceful_exit()

if __name__ == '__main__':
	from sys import argv
	try:
		main(argv[1:])
	except KeyboardInterrupt:
		print()
		exit()
