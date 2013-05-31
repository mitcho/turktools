*Turktools*
=========

Tools for preparing linguistic surveys for Amazon Mechanical Turk.

## Features

* Simplifies the **full workflow** for Turk-style experiment construction: randomized counterbalanced lists, local experiment simulation, and results in a format optimized for analysis
* **Template skeletons** which maximizes template reusability
* **Cross-platform** (Windows, Mac, and Linux), requiring only Python (2.6 or 2.7)
* **Simple tools** for non-programmers, with **command line options** for advanced users
* Experiments can be used **without Mechanical Turk**, with the use of [turkserver](https://github.com/mitcho/turkserver)

## Usage

To download everything here, click on the "ZIP" button above. The following tools are included:

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
 
* a *html skeleton* (an edited version of the *html skeletons* provided here, or created on your own), 
* an *html template* (created by the `templater.py`), 
* a raw items file
* a `xxxxxx.turk.csv` randomized items file (created by the `lister.py`), 
* a simulation of one or more of your lists (created by `simulator.py`),
* a raw results file (downloaded from AMT or from [turkserver](https://github.com/mitcho/turkserver)), 
* a decoded `xxxxxx.decoded.csv` results file (created by the `decoder.py`), and 
* an R analysis script (based on the sample `analysis.r` code provided here).

### Skeletons

A *skeleton* is an *html* file that contains substitution tags that will be filled in by the *Templater* to create a *html template* that can be uploaded onto AMT. The following template skeletons, accommodating the experimental designs indicated here, are currently included in *turktools*:

* `binary.skeleton.html`: Basic forced choice between two options: natural or unnatural.
* `binary-image.skeleton.html`: Truth value judgment paradigm with a sentence and an image presented. Forced choice true or false.
* `completion.skeleton.html`: Sentence completion with a gap and two options presented as radio buttons below.
* `completion-menu.skeleton.html`: Sentence completion with a gap and two options presented as a drop-down menu *in-situ*.
* `image-choice.skeleton.html`: Forced choice between three images. Can be used to generate covered-box experiments as well.
* `likert.skeleton.html`: Basic Likert scale template.
* `sentence-choice.skeleton.html`: Forced choice between two variable options, given a context.

The substitution tags in the *skeleton*, wrapped in double curly braces, i.e. `{{…}}`, will be filled in by the *Templater*. The skeletons all share the same basic structure: they include an experiment code, an instruction block with practice items, a consent statement, an items block, and demographic questions. At the bottom is a counter to help participants ensure that they have answered all the questions in the survey. The items block, beginning with `{{#items}}` and ending with `{{/items}}`, contains one sample item of the shape that all items in the survey will take. The items in your experiment can contain as many *fields* as necessary for your experiment. When a template is created out of the skeleton, the items block will be duplicated as many times as there are items in your survey.

Choose an appropriate *skeleton* for your experiment and edit it in a text editor such as [Notepad++](http://notepad-plus-plus.org/) (for Windows) [TextWrangler](http://www.barebones.com/products/textwrangler/) (for Mac), or create your own *skeleton* to accommodate a new type of experiment now supported by the *skeletons* above. Change the instructions, including any practice items, and add your consent statement and contact information for the experimenters. It is possible to add or remove questions and to change the order in which questions appear in your survey.  


### Templater

The *Templater* will take the skeleton you have edited and turn it into an *html template* that can be uploaded onto AMT.  

The *Templater* will ask for (a) the file name of your *skeleton*, (b) the total the number of items in your survey (including all experimental and filler items but not practice items, which are coded in the *skeleton*), and (c) a survey code: any letter-number combination you choose. 

The *Templater* will replace fields with `{{code}}` with the experiment’s unique code, `{{total_number}}` with the number of items presented in the experiment, and `{{number}}` with the item number in the experiment. The number will also appear in `{{field_n}}` tags. For example, for an item with two fields, the template will contain `field_n_1` and `field_n_2`, with *n* replaced by the appropriate number. 

### Lister



### Simulator

Once you have created a *html template* and a randomized `xxxx.turk.csv` items tile for your experiment, you are in principle ready to upload your experiment onto AMT. However, before doing so, we recommend simulating at least one of the lists in your experiment using `simulator.py`. The *Simulator* will ask you for (a) the file name of your *template*, (b) the file name of your `xxxx.turk.csv` items tile, and (c) which list you would like to simulate. It will create an *html* file that can be opened using any browser and will contain the experiment as it will be seen by participants who will participate in the list you chose. 

We recommend testing that the survey contain no errors: that the buttons or menus in the items work properly, that the counter is working, that all fields are shown properly and that *hidden fields* are *not* shown. We also recommend completing your own study at least once. This will give you a good idea of how long it takes to complete your study (that will also help determine payment on AMT) and whether you can detect other strategies for completing your study that are compatible with *satisfycing* behavior - that is, a strategy for solving the questions you are asking that does not involve performing the linguistic task that you are interested in.      

### Decoder

After uploading and running your survey, AMT will produce a *raw results file* which you can download from the `Manage` tab. The file will have a name like `Batch_999999_result.csv`. Save that file in your experiment's folder and then run `decoder.py` to convert this file into a format that can be read by statistical software such as *R*. 

The *Decoder* will ask for the file name and will produce a decoded `xxxxx.decoded.csv` results file that contains one row for each item in each survey that was submitted by any participant. The meta-data about the submission (including `AssignmentId`, `SubmissionStatus`, `WorkerId`, `WorkTimeInSeconds` and answers to demographic questions will be duplicated for each individual assignment, so you should have as many rows with this unique information as there were items in your experiment. For each item, information about the `Section`, `Condition`, `Item`, `List`, `PresentationOrder` and and ratings or answers to questions are logged. The *Decoder* also creates columns for *Factors* in the analysis based on your condition names, following the convention described above.  

### Analysis.R

As past of *turktools* we have provided a sample *R* analysis script that is able to take care of basic data filtering and preparation for statistical testing. The script implements several exclusion criteria and assists in basic data visualization. It also produces aggregate count data for your results. The script does not attempt to implement statistical tests, as those depend on the experimental design that you are using and on your research questions.   

### Additional reading

For a more detailed description of the tools and a proposed workflow for using them, please read: 

Erlewine, Michael Yoshitaka and Hadas Kotek (2013). [*A streamlined approach to online linguistic surveys*](lingbuzz submission link here). Submitted.

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

Contributions are welcome! Bug reports, feedback, documentation improvements, and code changes are all welcome forms of contributions. Thank you (in advance) for making *turktools* better for everyone.

#### Bug reports and feature requests:

New bug reports and feature requests can be added [on the turktools issue tracker](https://github.com/mitcho/turktools/issues?state=open). Please check whether your issue is already reported by someone else before opening a new issue. You must be logged into GitHub to create an issue.

#### Documentation:

[The turktools wiki](https://github.com/mitcho/turktools/wiki) on GitHub is open for ancillary documentation. If you are logged into GitHub, you can edit and create pages in the wiki. Feel free to contribute any materials there that you think may be helpful to a broader audience.

Changes to this main README file must be contributed as code changes, as described in the next section.

#### Contributing code:

turktools is developed [on GitHub](https://github.com/mitcho/turktools). The best way to hack on turktools is to open a GitHub account, [*fork* this repository](https://help.github.com/articles/fork-a-repo), and modify your own "fork" of the turktools. To submit changes, you can then initiate a [*pull request*](https://help.github.com/articles/using-pull-requests). Within reason, pull requests should include new [test cases](#testing), in order to avoid later regressions.

Contributors should be familiar with the [technical design goals](#design-goals) above.

### Testing [![Test Status](https://travis-ci.org/mitcho/turktools.png?branch=master)](https://travis-ci.org/mitcho/turktools)

turktools includes unit tests using the Python-standard `unittest` library. Tests can be run by running `python tests.py`. With the [`coverage`](http://nedbatchelder.com/code/coverage/) module installed, run `coverage run tests.py` and then use `coverage report -m` to see a code coverage report.

## Citations

If you use *turktools* or *turkserver* we ask that you cite Erlewine and Kotek (2013), [*A streamlined approach to online linguistic surveys*](link to lingbuzz submission here).    

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
