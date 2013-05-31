turktools
=========

Tools for preparing linguistic surveys for Amazon Mechanical Turk.

## Features

* Simplifies the **full workflow** for Turk-style experiment construction: randomized counterbalanced lists, local experiment simulation, and results in a format optimized for analysis
* **Template skeletons** which maximizes template reusability
* **Cross-platform** (Windows, Mac, and Linux), requiring only Python (2.6 or 2.7)
* **Simple tools** for non-programmers, with **command line options** for advanced users
* Experiments can be used **without Mechanical Turk**, with the use of [turkserver](https://github.com/mitcho/turkserver)

## Usage

To download everything here, click on the "ZIP" button above.

The following tools are included:

* `html skeletons`
* `templater.py`
* `simluator.py`
* `lister.py`
* `decoder.py`
* `analysis.r`: sample R analysis code

If you would like to host Mechanical Turk-style surveys on your own server instead of using Amazon Mechanical Turk, this can be done using turktools' sister project, [turkserver](https://github.com/mitcho/turkserver).

The python tools described here require Python 2.6.x or 2.7.x, available [here](http://python.org). Here is how to execute a Python script (here `templater.py`) in different platforms:

* **UNIX shell**: Move (cd) to the directory that contains the script and execute `python templater.py`.
* **Mac OS X**: Right-click on the file in the Finder and choose Open With… > `Python Launcher`.
* **Windows**: Double-click on the file.


## Setting up an experiment

We recommend saving all of the files you create for a given experiment in the same folder, dedicated to that experiment. By the time you're done preparing, running and analyzing an experiment, your folder for that experiment should include:
 
* a `html` skeleton (an edited version of the `html skeletons` provided here, or created on your own), 
* an `html` template (created by the `templater.py`), 
* a raw items file
* a `xxxxxx.turk.csv` randomized items file (created by the `lister.py`), 
* a simulation of one or more of your lists (created by `simulator.py`),
* a raw results file (downloaded from AMT or from [turkserver](https://github.com/mitcho/turkserver)), 
* a decoded `xxxxxx.decoded.csv` results file (created by the `decoder.py`, and 
* an R analysis script (based on the sample `analysis.r` code provided here).

### Template skeletons

A `skeleton` is an `html` file that contains substitution tags that will be filled in by the `Templater` to create a `html template` that can be uploaded onto AMT. The following template skeletons, accommodating the experimental designs indicated here, are currently included in *turktools*:

* `likert.skeleton.html`: Basic Likert scale template.
* `image-choice.skeleton.html`: Forced choice between three images.
* `binary.skeleton.html`: Basic forced choice between two options: natural or unnatural.
* `completion.skeleton.html`: Sentence completion with a gap and two options presented.
* `binary-image.skeleton.html`: Truth value judgment paradigm with a sentence and an image presented. Forced choice true or false.
* `sentence-choice.skeleton.html`: Forced choice between two variable options, given a context.

The substitution tags in the `skeleton`, all wrapped in double curly braces, i.e. `{{…}}`, will be filled in by the `Templater`. The skeletons all share the same basic structure: they include an experiment code, an instruction block with practice items, a consent statement, an items block, and demographic questions. At the bottom is a counter to help participants ensure that they have answered all the questions in the survey. The items block, beginning with `{{#items}}` and ending with `{{/items}}`, contains one sample item of the shape that all items in the survey will take. When a template is created out of the skeleton, this block will be duplicated as many times as there are items in your survey.

Choose an appropriate `skeleton` for your experiment and edit it in a text editor such as [Notepad++](http://notepad-plus-plus.org/) (for Windows) [TextWrangler](http://www.barebones.com/products/textwrangler/) (for Mac), or create your own `skeleton` to accommodate a new type of experiment now supported by the `skeletons` above. Change the instructions, including any practice items, and add your consent statement and contact information for the experimenters. It is possible to add or remove questions and to change the order in which questions appear.  


### Templater

The `Templater` will take the skeleton you have edited and turn it into an `html template` that can be uploaded onto AMT.  

The `Templater` will ask for file name of your `skeleton`, the total the number of items in your survey (including all experimental and filler items but not practice items, which are coded in the `skeleton`), and a survey code: any letter-number combination you choose. 

The `Templater` will replace fields with `{{code}}` with the experiment’s unique code, `{{total_number}}` with the number of items presented in the experiment, and `{{number}}` with the item number in the experiment. The number will also appear in `{{field_n}}` tags. For example, for an item with two fields, the template will contain `field_n_1` and `field_n_2`, with *n* replaced by the appropriate number. 

### Lister

### Simulator

### Decoder

### Analysis.R






## Testing

[![Test Status](https://travis-ci.org/mitcho/turktools.png?branch=master)](https://travis-ci.org/mitcho/turktools)

turktools includes unit tests using the Python-standard `unittest` library. Tests can be run by running `python tests.py`. With the [`coverage`](http://nedbatchelder.com/code/coverage/) module installed, run `coverage run tests.py` and then use `coverage report -m` to see a code coverage report.

## The MIT License (MIT)

Copyright (c) 2013 Michael Yoshitaka Erlewine <mitcho@mitcho.com> and contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
