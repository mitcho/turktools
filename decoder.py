# coding: utf-8
"""
turkolizer decoder
mitcho (Michael Yoshitaka Erlewine), mitcho@mitcho.com, April 2013

Uses a Turkolizer decode file to decode a Turk results file.
"""

"""
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

from os.path import splitext
from sys import argv
from csv import DictReader, DictWriter
import re
from platform import system

def graceful_exit():
	if system() == 'Windows':
		raw_input('Press enter to close the window...')
	exit()

def graceful_read_csv(filename):
	data = []
	try:
		f = open(filename, 'rb')
	except IOError as e:
		print "ERROR: ", e.strerror
		graceful_exit()

	csvreader = DictReader(f)
	while True:
		try: row = csvreader.next()
		except: break
		data.append(row)

	return data

results = argv[1] if len(argv) > 2 else raw_input("Please enter the Turk results file name: ")
decode = argv[2] if len(argv) > 2 else raw_input("Please enter the Turkolizer decode file name: ")

decode_data = graceful_read_csv(decode)

if len(decode_data) == 0:
	print "It looks like this decode file is not formatted correctly. Please try again."
	graceful_exit()

# todo: is there a better way to get the trial_numbers and check it?
trial_numbers = [int(re.sub(r'^Item(\d+)$', '\\1', key)) for key in decode_data[0].keys() if re.search(r'^Item(\d+)$', key)]
trial_numbers.sort()
if min(trial_numbers) != 1 or max(trial_numbers) != len(trial_numbers):
	print "It looks like this decode file is not formatted correctly. Please try again."
	graceful_exit()

# turn the decode_data into a hash, for lookup by list
# todo: rewrite this so it's not a dict comprehension? maybe this is hard to read...
decode_data = {int(row['list']):
		{n:
			{
				'Section': row['Section' + str(n)],
				'Item': int(row['Item' + str(n)]),
				'Condition': row['Condition' + str(n)],
				'PresentationOrder': n
			}
		for n in trial_numbers}
	for row in decode_data}

results_data = graceful_read_csv(results)

if len(results_data) == 0:
	print "It looks like this results file is missing data or is not formatted correctly. Please try again."
	graceful_exit()

for expected in ['Title', 'Description', 'Keywords', 'Reward']:
	if expected not in results_data[0]:
		print "It looks like the results file is not formatted correctly (missing expected column {0}). Please try again.".format(expected)
		graceful_exit()

print '-------------'
print 'Title:       ', results_data[0]['Title']
print 'Description: ', results_data[0]['Description']
print 'Keywords:    ', results_data[0]['Keywords']
print 'Reward:      ', results_data[0]['Reward']
print '-------------'

decoded_data = []

re_extra = re.compile('^Answer\.(\D+)$');
for n in trial_numbers:
	re_input = re.compile('^Input\.trial_' + str(n) + '_(\d+)$');
	re_answer = re.compile('^Answer\.(\w*?\D)_?' + str(n) + '$');
	re_sample = re.compile('^Answer\.(\w*?\D)_?Sample' + str(n) + '$');
	for row in results_data:
		list_number = int(row['Input.list'])

		# this line does the merge, basically:
		data = decode_data[list_number][n].copy()
		data['ListNumber'] = list_number
		
		# copy user/assignment meta		
		data['WorkerId'] = row['WorkerId']
		data['AssignmentId'] = row['AssignmentId']
		data['AssignmentStatus'] = row['AssignmentStatus']
		data['WorkTimeInSeconds'] = row['WorkTimeInSeconds']

		for field in row.keys():
			if re_input.match(field) is not None:
				data[re_input.sub('field_\\1', field)] = row[field]
			if re_answer.match(field) is not None and re_sample.match(field) is None:
				data[re_answer.sub('\\1', field)] = row[field]
			if re_extra.match(field):
				data[re_extra.sub('\\1', field)] = row[field]				

		# todo: get sample/practice item answers?
		decoded_data.append(data.copy())

# todo: check that each row has the same number of fields!

name_part, extension = splitext(results)
filename = name_part + '.decoded.csv'

import csv
with open(filename, 'wb') as f:
	keys = decoded_data[0].keys()
	keys.sort()
	# be smarter about key sort?
	writer = DictWriter(f, keys, extrasaction = 'ignore')
	writer.writeheader()
	for row in decoded_data:
		writer.writerow(row)

print 'Successfully wrote decoded results to ' + filename
graceful_exit()
