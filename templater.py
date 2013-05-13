# coding: utf-8
"""
Turk Templater
mitcho (Michael Yoshitaka Erlewine), mitcho@mitcho.com, March 2013

Renders Mechanical Turk template "skeletons" using the "mustache" templating language:
  http://mustache.github.com/mustache.5.html

Turk fields will be of the form ${trial_i_j}, where i is the trial number and j is 
a unique integer. This matches the output of the Lister.

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
import os, inspect
from sys import path
import atexit

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

# add pystache submodule to path
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join('.', 'ext', 'pystache')))
if cmd_subfolder not in path:
	path.insert(0, cmd_subfolder)
from pystache import render

def graceful_read(filename):
	try:
		return open(filename, 'r').read()
	except IOError as e:
		print( "ERROR:", e.strerror )
		exit()

maximum_number_of_fields = 100 # reasonable enough, I think.

def main(template, template_string, number, code):
	name_part, extension = os.path.splitext(template)
	filename = name_part.replace('.skeleton', '') + '-' + code + '-' + str(number) + extension
	output_file = open(filename, 'w')

	def item(i):
		i = str(i)
		basic = {
			'number': i, 
			'field': '${trial_' + i + '_1}',
		}
		fields = {}
		for j in range(1, maximum_number_of_fields):
			fields[ 'field_' + str(j) ] = '${trial_' + i + '_' + str(j) + '}'

		return dict( basic.items() + fields.items() )

	obj = {
		'total_number': number,
		'code': code,
		'items': [ item(i) for i in range(1, number + 1) ]
	}
	output_file.write(render(template_string, obj))

	print( 'Successfully wrote template to ' + filename )
	exit()

if __name__ == '__main__':
	from sys import argv

	template_string = ''
	if len(argv) > 1:
		template = argv[1]
		template_string = graceful_read(template)

	while '{{' not in template_string:
		if template_string != '':
			print( "This file doesn't look like a skeleton file!" )
		template = raw_input("Please enter the skeleton file name: ")
		template_string = graceful_read(template)

	number   = int(argv[2]) if len(argv) > 2 else int(raw_input("Please enter the number of items: "))
	code     = argv[3]      if len(argv) > 3 else raw_input("Please enter the survey code: ")

	main(template, template_string, number, code)
