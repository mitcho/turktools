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
import re, atexit, readline

@atexit.register
def graceful_exit():
	from platform import system
	if system() == 'Windows':
		raw_input('Press enter to close the window...')

# adds tab completion to raw_input, for those platforms that support it
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

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

class Trial:
	def __init__(self, section, number, condition):
		self.section = section
		self.number = int(number)
		self.condition = condition
		self.fields = []
	def __repr__(self):
		return "[Trial {0.section} {0.number} {0.condition} ({1})]".format(self, len(self.fields))

def graceful_read_items(filename):
	f = open(filename, 'r')

	items = []
	
	# header lines must have: ^# section number condition$
	header_pattern = re.compile(r'^#\s+(\S+)\s+(\d+)\s+(.*?)\s*$')
	
	current_trial = False
	for line in f:
		line = line.strip()
		
		if line == '':
			continue
	
		matched = header_pattern.match(line)
		
		if matched is False and current_trial is False:
			# skip these lines. todo: print an error?
			print('weird')
		
		if matched:
			section, number, condition = matched.groups()
			# print(section, number, condition)
			current_trial = Trial(section, number, condition)
			items.append(current_trial)
		else:
			current_trial.fields.append(line)
	
	return items

def main(items_file, lists):
	items = graceful_read_items(items_file)
	print(items)

	name_part, extension = splitext(items_file)

if __name__ == '__main__':
	from os.path import splitext
	from sys import argv

	items_file = argv[1] if len(argv) > 2 else raw_input("Please enter the items file name: ")
	lists = argv[2] if len(argv) > 2 else raw_input("How many lists would you like to create: ")

	# todo: other parameters later?
	main(items_file, lists)
