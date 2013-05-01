Turk Tools
==========

Tools to prepare linguistic surveys for Amazon Mechanical Turk.

Copyright 2013 Michael Yoshitaka Erlewine <mitcho@mitcho.com> and contributors. All code licensed under the MIT license. See license block below and in individual files.

To download everything here, click on the "ZIP" button above.

## Design goals

TODO

## Tools

The following tools are currently distributed in this repository:

* `templater.py`
* `simluator.py`
* `decoder.py`
* `analysis.r`: sample R analysis code

The tool `turkolizer.py` is *not* included in this repository, due to an unclear software license. Contact mitcho to get the latest version of the turkolizer. In the near future, I will probably do a clean-room-rewrite of this tool so it can be released in the open without copyright constraints.

## Usage

TODO

## Template skeletons

The `templater.py` tool takes "skeletons" of templates and turns them into templates which are ready for use on Turk, with the right number of fields. The following template skeletons are currently included here:

* `likert.skeleton.html`: Basic Likert scale template.
* `image-choice.skeleton.html`: Forced choice between three images.
* `binary.skeleton.html`: Basic forced choice between two options: natural or unnatural.
* `completion.skeleton.html`: Sentence completion with a gap and two options presented.
* `binary-image.skeleton.html`: Truth value judgment paradigm with a sentence and an image presented. Forced choice true or false.
* `sentence-choice.skeleton.html`: Forced choice between two variable options, given a context.

## References

TODO

## The MIT License (MIT)

Copyright (c) 2013 Michael Yoshitaka Erlewine and contributors

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
