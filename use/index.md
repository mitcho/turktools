---
title: Instructions
layout: default
---

To download everything here, click on the "Download ZIP" button on the left. The following tools are included:

* Sample HTML skeletons
* `templater.py`
* `simluator.py`
* `lister.py`
* `decoder.py`
* `analysis.r`: sample R analysis code

We have additionally provided sample item files for three of the skeletons in the Examples folder. 

If you would like to host Mechanical Turk-style surveys on your own server instead of using Amazon Mechanical Turk, this can be done using turktools' sister project, [turkserver](https://github.com/mitcho/turkserver).

The Python tools described here require Python 2.6.x or 2.7.x, available [here](http://python.org). Here is how to execute a Python script (here `templater.py`) in different platforms:

* **UNIX shell**: Move (`cd`) to the directory that contains the script and execute `python templater.py`.
* **Mac OS X**: Right-click on the file in the Finder and choose Open With… > Python Launcher.
* **Windows**: Double-click on the file.

We recommend saving all of the files you create for a given experiment in the same folder, dedicated to that experiment.

In the remainder of this section, we will describe the usage of these tools. For a more detailed description of the tools and a proposed workflow, please read:

> Erlewine, Michael Yoshitaka and Hadas Kotek (2013). [*A streamlined approach to online linguistic surveys*](http://ling.auf.net/lingbuzz/001802/current.pdf). Manuscript, MIT.

### Skeletons

A *skeleton* is an HTML file that contains substitution tags that will be filled in by the *Templater* to create an *HTML template* that can be uploaded onto AMT. The following template skeletons are currently included in *turktools*, each corresponding to a different experimental design:

* `binary.skeleton.html`: Basic forced choice between two options: natural or unnatural.
* `binary-image.skeleton.html`: Truth value judgment paradigm with a sentence and an image presented. Forced choice true or false.
* `completion.skeleton.html`: Sentence completion with a gap and two options presented as radio buttons below.
* `completion-menu.skeleton.html`: Sentence completion with a gap and two options presented as a drop-down menu *in-situ*.
* `image-choice.skeleton.html`: Forced choice between three images. Can be used to generate covered-box experiments as well.
* `likert.skeleton.html`: Basic Likert scale template.
* `sentence-choice.skeleton.html`: Forced choice between two options, given a context.

The skeleton contains substitution tags, wrapped in double curly braces, i.e. `{% raw %}{{…}}{% endraw %}`, will be filled in by the *Templater*. [Read more about the supported substitution tags](tags.html).

The provided skeletons all share the same basic structure: they include an experiment code, an instruction block with practice items, a consent statement, an items block, and demographic questions. At the bottom is a JavaScript counter to help participants ensure that they have answered all the questions in the survey. The items block, beginning with `{% raw %}{{#items}}{% endraw %}` and ending with `{% raw %}{{/items}}{% endraw %}`, contains one sample item of the shape that all items in the survey will take. The item block will contain `{% raw %}{{field_n}}{% endraw %}` tags, corresponding to different *fields* in your items. (See the items file section below for more on fields.) When a template is created out of the skeleton, the items block will be duplicated as many times as there are items in your survey.

Choose an appropriate skeleton for your experiment and edit it in a text editor such as [Notepad++](http://notepad-plus-plus.org/) (for Windows) or [TextWrangler](http://www.barebones.com/products/textwrangler/) (for Mac), or create your own to accommodate a different type of experiment. Change the instructions, including any practice items, and add your consent statement and contact information for the experimenters. Everything about the experiment's layout, design, and presentation can be changed by modifying the skeleton.

### Templater

The *Templater* will take the skeleton you have edited and turn it into an HTML *template* that can be uploaded onto AMT.  

The *Templater* will ask for (a) the file name of your *skeleton*, (b) the total number of items in your survey (including all experimental and filler items but not practice items, which are coded in the skeleton), and (c) a survey code: any letter-number combination you choose. The *Templater* will then generate a template from your skeleton.

### The items file

*Lister* creates randomized items lists out of an *items file* that must be formatted a certain way.

Each item in the raw items file has two parts, each beginning on a new line. 

* **The item header.** The item header consists of four components, separated by space:
	* the symbol #;
	* the name of the section (e.g., target, filler);
	* the item set number within the section (we recommend 1, 2, 3, …);
	* the condition name
* **The item body.** The item body consists of fields, each on its own line. Line *n* corresponds to the text that will be substituted for the text `{% raw %}{{field_n}}{% endraw %}` in your HTML template. A field may specify a sentence to be judged, choices for completions, a picture, an audio file, a context, a comprehension question, etc.

Condition names are not constrained in any way, but we recommend a naming convention where the values for each of your experimental factors is listed and separated from other values by a hyphen:

> `<factor 1 value>-<factor 2 value>-<factor 3 value>-...`

The *Decoder* tool will create separate factors from the Condition names when it is run. Note that all items in a given experimental section must have the same number of conditions, but it is not necessary to keep the same names. As long as each item set has the same number of conditions, you can use different names across different item sets. The *Lister* will produce a warning when it is run, but you may choose to proceed.

Each item must specify information for at least as many fields as there are in the HTML template that you'll be using. It is possible to have *hidden fields* that do not correspond to fields in the template. Those fields will not be shown to participants but they will be carried over to the randomized file and to the results file. You can use hidden fields to specify expected correct answers to fillers or comprehension questions, and once you have a results file it will be easy to calculate accuracy for your participants.

You can find sample items file that match the `binary.skeleton.html`, the `binary-image.skeleton.html` and the `completion.skeleton.html` in the Examples folder. 

### Lister

`lister.py` takes an *items file* and turns it into a `xxxxxx.turk.csv` file with randomized lists of items, that can be uploaded onto AMT. The *Lister* creates Latin Square counterbalanced randomized lists from the items that it is given.

Once it is run, `lister.py` will ask for (a) the name of your raw items file, (b) which sections should be treated as fillers, (c) how many filler items you would like placed between each target item, (d) how many filler items you would like placed in the beginning and end of the experiment, (e) how many lists you would like to create, and (f) whether or not you would like the reverse of each list to also be created, to help reduce any ordering effects that may occur.

Note that as a default, no section is singled out to be used as fillers. You may to designate one or more sections as fillers and all the other sections will be treated as targets. Fillers and targets will be randomized separately and then combined according to the conditions you specified.
   

### Simulator

Once you have created an HTML template and a randomized `xxxxxx.turk.csv` items list file for your experiment, you are in principle ready to upload your experiment onto AMT. However, before doing so, we recommend simulating at least one of the lists in your experiment using `simulator.py`. The *Simulator* will ask you for (a) the file name of your *template*, (b) the file name of your `xxxxxx.turk.csv` items list file, and (c) which list you would like to simulate. It will create a *simulation* HTML file that can be opened using your web browser and will contain the experiment as it will be seen by your participants.

We recommend simulating the survey to verify that it does not contain any errors: that the buttons or menus in the items work properly, that the counter is working, that all fields are shown properly and that *hidden fields* are *not* showing. We also recommend completing your own study at least once. This will give you a good idea of how long it takes to complete your study (which will also help determine payment on AMT) and whether you can detect other strategies for completing your study that are compatible with [*satisfycing*](https://en.wikipedia.org/wiki/Satisficing) behavior - that is, a strategy for solving the questions you are asking that does not involve performing the linguistic task that you are interested in.

### Decoder

After uploading and running your survey, AMT will produce a *raw results file* which you can download from the `Manage` tab. The file will have a name like `Batch_999999_result.csv`. Save that file in your experiment's folder and then run `decoder.py` to convert this file into a format that can be easily read and analyzed in statistical software such as [R](http://www.r-project.org/).

The *Decoder* will ask for the results file name and will produce a decoded `xxxxxx.decoded.csv` results file that contains one row for each item in each submission. The metadata about the submission (including `AssignmentId`, `SubmissionStatus`, `WorkerId`, `WorkTimeInSeconds` and answers to demographic questions) will be duplicated across all rows within an individual assignment, so each of these values will be in as many rows as there were items in your experiment. For each item, information about the `Section`, `Condition`, `Item`, `List`, `PresentationOrder` and and ratings or answers to questions are logged. The *Decoder* also creates columns for *factors* in the analysis based on your condition names, following the convention described above.

### analysis.r

As past of *turktools* we have provided a sample analysis script  for [R](http://www.r-project.org/) that takes care of basic data filtering and preparation for statistical testing. The script implements several exclusion criteria and assists in basic data visualization. It also produces aggregate count data for your results. The script does not attempt to implement statistical tests, as those depend on the experimental design that you are using and on your research questions.

### At the end of the day...

By the time you're done preparing, running, and analyzing an experiment, your folder for that experiment will include:
 
* an *HTML skeleton* (an edited version of the HTML skeletons provided here, or created on your own), 
* an *HTML template* (created by `templater.py` from your skeleton), 
* a text file with your raw items
* a `xxxxxx.turk.csv` randomized item lists file (created by `lister.py`),
* a simulation of one or more of your lists (created by `simulator.py`),
* a raw results file (downloaded from AMT or from [turkserver](https://github.com/mitcho/turkserver)), 
* a decoded `xxxxxx.decoded.csv` results file (created by `decoder.py`), and 
* an analysis script (possibly based on the sample `analysis.r` code provided here).
