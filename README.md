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

The `templater.py` tool takes "skeletons" of templates and turns them into templates which are ready for use on Turk, with the right number of fields. The following template skeletons are currently included in the `skeletons` directory:

* `binary.skeleton.html`: Basic forced choice between two options: natural or unnatural.
* `binary-image.skeleton.html`: Truth value judgment paradigm with a sentence and an image presented. Forced choice true or false.
* `completion.skeleton.html`: Sentence completion with a gap and two options presented as radio buttons below.
* `completion-menu.skeleton.html`: Sentence completion with a gap and two options presented as a drop-down menu *in-situ*.
* `image-choice.skeleton.html`: Forced choice between three images. Can be used to generate covered-box experiments as well.
* `likert.skeleton.html`: Basic Likert scale template.
* `sentence-choice.skeleton.html`: Forced choice between two variable options, given a context.

## Known issues

* [Issue #1](https://github.com/mitcho/turktools/issues/1): Input files must be ASCII. Full Unicode support is planned.
* [Issue #2](https://github.com/mitcho/turktools/issues/2): If the results CSV file from Turk is modified and saved in Excel, `decoder.py` will not be able to read it. This has to do with the line-endings which are used by Excel's CSV output.

## Technical information

### Design goals

turktools is designed with the non-technical user in mind. Therefore, the following principles are adopted in its design and development:

* **Be portable**: each tool is a stand-alone script, and can be moved or copied to a different filesystem location and continue to function.
* **Be graceful**: catch failures and present useful warnings and errors to the user.
* **No dependencies**: just Python, out of the box.

The current development target is Python 2.6 and 2.7. Python 3 support [would be great in the future](https://github.com/mitcho/turktools/issues/3).

Note that an unfortunate consequence of the portability goal is to explicitly eschew a shared code library, forcing code duplication across different scripts, in violation of [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself). The current approach is to at least ensure the integrity of duplicated code across tools, by subjecting them to the exact same [tests](#testing). (Perhaps a build tool will be used in the future to cut down on such redundancies.) Note also that the no dependencies goal and Python 2.6 target means that nice libraries like `argparse` cannot be used.

### Contributing

Contributions are welcome! Bug reports, feedback, documentation improvements, and code changes are all welcome forms of contributions. Thank you (in advance) for making turktools better for everyone.

_Bug reports and feature requests:_

New bug reports and feature requests can be added [on the turktools issue tracker](https://github.com/mitcho/turktools/issues?state=open). Please check whether your issue is already reported by someone else before opening a new issue. You must be logged into GitHub to create an issue.

_Documentation:_

[The turktools wiki](https://github.com/mitcho/turktools/wiki) on GitHub is open for ancillary documentation. If you are logged into GitHub, you can edit and create pages in the wiki. Feel free to contribute any materials there that you think may be helpful to a broader audience.

Changes to this main README file must be contributed as code changes, as described in the next section.

_Contributing code:_

turktools is developed [on GitHub](https://github.com/mitcho/turktools). You can hack on turktools using [the Fork & Pull model](https://help.github.com/articles/using-pull-requests#fork--pull). The best way to submit code is to then initiate a [*pull request*](https://help.github.com/articles/using-pull-requests).

Within reason, pull requests should include their own [tests](#testing), in order to avoid later regressions.

Contributors should be familiar with the [technical design goals](#design-goals) above.

### Testing

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
