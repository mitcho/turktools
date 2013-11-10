---
title: Using Mechanical Turk
layout: default
---

### Uploading surveys onto AMT

After verifying that the survey is ready, it can be uploaded onto AMT. To do so, it is necessary to create an account and log in to [AMT](https://www.mturk.com/mturk/welcome) as a requester. You can create a new project through the Create tab. The creation of a new project involves three steps: in the first screen, choose a name and description for your project and decide on number of workers and payment.  At this point, certain restrictions can be placed on the workers who will be offered this HIT. For example, it is often useful to restrict IP addresses of workers to a certain country or region or to request workers with a high approval rate. In the second screen, the template is uploaded. 

Click on 'Edit HTML Source', then open your template file in a text editor and copy all of its contents into the edit screen. Save this change, preview the resulting template in the third screen and finish. After creating a new project, you must upload your randomized lists file as a ‘New Batch.’ After you click the button, a window will open that will allow you to choose your `xxxxxxxx.turk.csv` file. Make sure that the surveys render properly and that the payment is appropriate, and post your study. 

### Downloading the results of surveys from AMT

The results file is obtained through the Manage tab on AMT. You should visit the Manage tab while your survey is in progress to check on its progress, and approve or reject the results of the workers who have participated in your study. Before doing so, we recommend first downloading the results file (by clicking the ‘Download CSV’ button) in order to scrutinize your participants’ behavior more closely. The results of a AMT survey are saved in the form of a `.csv` file with a name like `Batch_999999_result.csv`. This raw results file consists of a header row with the names of each of its columns, followed by one row for each participant’s values for each of the columns. In addition to participants’ responses to the experimental items, the raw results file also contains information about the submission such as time of submission, duration of the experiment, time of approval, approval/rejection rate, etc.

In some cases it may be necessary to reject submissions from workers who have completed more than one survey (see the [basic analysis suggestions](analysis.html) page). It may also be desirable to reject workers with low accuracy on comprehension questions and ‘catch’ filler items and those workers who failed to complete at least 80% of the study. To quickly identify workers who completed more than one survey, open the file in software such as Excel and sort by `WorkerId`. For suggestions for additional exclusion criteria and how to identify workers who meet them using R, see Section 11 below. Once you have decided which workers to approve and which to reject, return to the Manage tab in your AMT webpage and approve or reject your workers there. In order to maintain a positive reputation as a requester on AMT, it is advisable to approve submissions in a timely fashion and to maintain a low rejection rate. 
