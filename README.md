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

* `templater.py`
* `simluator.py`
* `lister.py`
* `decoder.py`
* `analysis.r`: sample R analysis code

TODO: describe usage

If you would like to host Mechanical Turk-style surveys on your own server instead of using Amazon Mechanical Turk, this can be done using turktools' sister project, [turkserver](https://github.com/mitcho/turkserver).

## Template skeletons

The `templater.py` tool takes "skeletons" of templates and turns them into templates which are ready for use on Turk, with the right number of fields. The following template skeletons are currently included here:

* `likert.skeleton.html`: Basic Likert scale template.
* `image-choice.skeleton.html`: Forced choice between three images.
* `binary.skeleton.html`: Basic forced choice between two options: natural or unnatural.
* `completion.skeleton.html`: Sentence completion with a gap and two options presented.
* `binary-image.skeleton.html`: Truth value judgment paradigm with a sentence and an image presented. Forced choice true or false.
* `sentence-choice.skeleton.html`: Forced choice between two variable options, given a context.

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
