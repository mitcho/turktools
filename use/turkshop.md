---
title: Notes for MIT Turkshop participants
layout: default
---

Participants of the Spring 2013 Turkshop at MIT used a pre-release version of *turktools*. *turktools* are largely compatible with the version of the tools we presented at the workshop, but there are some changes. Below is a summary of the differences between the pre-release version and the current *turktools*.

### Conceptualization and preparation of items

Nothing here has changed. All your old items files should be compatible with the new tools. 

Note that we have added the option of *hidden fields*, which did not exist before. Hidden fields allow you to save as part of your experiment information that you do not want to show to participants but you would still like to have handy for the analysis. For example, you can use a hidden field to indicate expected correct answers to filler items or to comprehension questions. A hidden field is any field that does not have a corresponding field in your template. So if your template had `{% raw %}{{field_1}}` and `{{field_2}}{% endraw %}`, anything in the third line and onward of each item block in your items file will be hidden. See more on hidden fields in the Readme.

We now recommend using the Condition naming convention that we introduced in class as a rule: 
> `<factor 1 value>-<factor 2 value>-<factor 3 value>-...`

The *Decoder* will automatically create separate columns for each of your factors in your results file, so you don't have to deal with any regular expressions yourself. 

*Stay tuned* for the option of using separators other than `-` in condition names, including a SPACE. 


### Skeletons 

Skeletons with a drop-down menu and with a Likert scale have been added. The biggest difference in the skeletons is that we are now using the tag `{% raw %}{{field_n}}` instead of `{{trial_n}}{% endraw %}` in the older versions. This means that your old skeletons will **not** be compatible with the new tools -- you'll have to download the new skeletons and copy your existing content (instructions, practice items, consent statement, etc) into the new version. 

### Templater

The *Templater* now allows for *hidden fields*, as mentioned above, and it requires the tag `{% raw %}{{field_n}}` instead of `{{trial_n}}{% endraw %}`. Aside from that, using the *Templater* is no different than it was before. 

### Simulator

Nothing changed here. 

### Lister

The *Lister* is now our tool for generating randomized lists and it has been written from scratch since the Turkshop. You now have the option not to create the reverse of your lists, so the minimum number of lists created is the smallest multiple of the number of conditions in your different sections. 

An important change is that in the new *Lister*, no section is singled out to act as fillers. The *Lister* will ask you which sections to treat as fillers, and you can choose any number of sections for that purpose. All the sections not designated as fillers will be treated as targets; the targets and the fillers will be randomized within themselves and then fillers will be distributed between the targets according to your requests (you can specify how many fillers should appear between each two target items and at the beginning and end of the list). You can also choose not to have any fillers or to have less fillers than targets. 

The output of the *Lister* is just one file, the randomized `xxxxx.turk.csv` file. There is no `xxxxx.decode.csv` file anymore. 

### Decoder 

The *Decoder* now requires just one file - the raw results file downloaded from AMT after you have run your experiment. You don't need to also give the *Decoder* a `xxxxx.decode.csv` file (note that such a file is no longer created by the *Lister*). 

The *Decoder* will automatically create separate columns for each of your *factors* based on your condition names. For condition names that look as shown above, three columns will be created: `Factor_1`, `Factor_2`, and `Factor_3`, with the corresponding values for each item stored in the appropriate cells. 

Note that the new *Decoder* is **not** compatible with results files from experiments that were run during Turkshop. If you need to decode an old results file, contact us for a version of the old *Decoder*. 

### Analysis

Not much has changed. The same basic script that we have used to help some participants look at their data still exists, but the process of using the script is simplified. You only need to read in the decoded results file, and all the information you need should be there. Instead of needing to create a separate file for expected correct answers and merging it with the results, you should now have that information in hidden fields in your decoded results file. There is code to calculate participants' accuracy based on these hidden fields. Your factors will already be coded as well, and there is a command that will help you rename the factors to give them more meaningful names based on your experiment. This saves you having to use regular expressions yourself. We have also implemented some additional basic graphics that we did not show in class. 
