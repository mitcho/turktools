---
title: Basic suggestions for data analysis
layout: default
---

### Some analysis suggestions

A full discussion of R and statistical analysis methods is beyond the scope of this post. The statistical analysis used for an experiment must fit the design of that experiment and its research question. For more detailed reading on data analysis, see DeGroot et al. (1986) for statistics; Gelman and Hill (2007) for regression; Baayen et al. (2008), Bates and Maechler (2009) and Barr et al. (2013) for mixed effects regressions; and Venables and Ripley (2000) and Baayen (2008) for R. 

Here we suggest some suggestions for simple first steps of looking at your data in R.

### Data preparation: Eliminating data from bad submissions

Before analyzing the results of your experiment, it is useful to prepare the data for analysis. Here are suggestions for steps that may be useful to follow, implemented in R. R is free, open-source statistics software available from [http://www.r-project.org/](http://www.r-project.org/). We recommend using RStudio, freely available at [http://www.rstudio.com/ide/download/desktop](http://www.rstudio.com/ide/download/desktop), rather than the R console itself. You will need to have R installed on your computer to use RStudio. We recommend using the packages `languageR` for simple analyses and `lattice` for data visualization; these packages are available from CRAN ([http://cran.r-project.org/](http://cran.r-project.org/)), the Comprehensive R Archive Network. Packages can be installed using the R command install.packages or through the command `Install Packages` in the Tools menu in RStudio. To read more about this and any other functions in R, type a question mark before the function name into the R console, e.g. `?install.packages`, or go to the Help tab in the lower right-hand side of your screen in RStudio.

Once RStudio is running, you can create or edit an analysis script for your experiment. We have provided as part of the tools in this paper a simple analysis script `analysis.r` that you can modify for your needs. We recommend keeping the script in the same folder as the other scripts and data for your experiment. We further recommend having separate directories for each experiment that you create. It is better to edit analysis scripts rather than typing commands directly into the R-Studio (or R) console, because having a script ensures replicability and creates a record of your work. 

After saving your analysis script in the same folder as the decoded results file, set the Working Directory to the source file location. This can be done from the Tools menu in RStudio or by using the command `setwd(‘xxxxxx’)`, where xxxxxx is the full path to the directory where your results file is located on your computer. 

Start by reading in the decoded results file into a variable, here results. 
	results <- read.csv('definiteness-effect.results.decoded.csv', header=TRUE)

We recommend cleaning up this file in at least four ways, by excluding the following types of participants: (a) non-native speakers, (b) participants whose submission you rejected on AMT, (c) participants who did not complete the survey and participants who completed more than one survey, (d) participants with low accuracy rates on ‘catch’ filler items and comprehension questions. Depending on the study, you may choose to use only some of the suggestions in (a)-(d) and perhaps to use other additional exclusion criteria. Normally, we find that few participants need to be filtered from an experiment—usually fewer than 10%.

Non-native speakers can be excluded by applying the subset command to the results file and keeping only participants who said that they are native speakers (in this case, of English). We will use the answer given to one of the demographic questions in our skeletons, stored in the english column. The subset command will take a data frame and a criterion and return only those lines in the data frame that meet the criterion.

	results <- subset(results, english == 1)

To reject participants whose submission you rejected on AMT, subset the file to return only those participants whose assignment status is not 'Rejected'.

	results <- subset(results, AssignmentStatus != 'Rejected')

It is up to the researcher to decide how many missed items are too many and whether or not to reject participants who completed more than one survey. Below is a suggestion for rejecting anyone who completed more than one study or completed less than 80% of the study. Other values for `notEnough` can be used by replacing `0.8*surveyLength` with any other setting.

	results$isNA <- ifelse(is.na(results$Choice) | results$Choice == '', 0, 1)
	howMany <- aggregate(results$isNA, list(results$WorkerId), sum)
	surveyLength <- as.numeric(aggregate(results$AssignmentId, by=list(results$AssignmentId), length)$x[1])
	notEnough <- 0.8*surveyLength
	didTooMany <- subset(howMany, x > surveyLength)$Group.1
	didntDoEnough <- subset(howMany, x < notEnough)$Group.1
	results <- subset(results, !(WorkerId %in% didTooMany))
	results <- subset(results, !(WorkerId %in% didntDoEnough))

Finally, compute accuracy on comprehension questions and filler items that had expected values. Gibson et al. (2011) recommend only accepting results from participants whose accuracy on such items is at least 75%, unless there is a substantial number of participants whose performance was below this rate. Because there are no memory demands in most linguistic surveys, a 75% accuracy rate should be easy for conscientious native speaker participants to achieve. If there are many participants who did not achieve this success rate, however, it is possible that there was something wrong with the answers to your survey and we recommend that you inspect your items before deciding to reject workers on AMT based on their accuracy.

If expected correct answers were included in hidden fields in your items file, they can easily be compared to the answers provided by participants in your study. For example, if expected answers to fillers were specified in the fifth line of their item bodies, it will be stored in the decoded results file in column `field_5`. The following code uses this to compute accuracy rates per participant and reject those whose accuracy rate is below 75%. You should inspect accuracy to see if any filler item had low accuracy rates and, if so, exclude it from the accuracy calculation. 

	results$isCorrect <- ifelse(is.na(results$field_5), NA, ifelse(results$field_5 == results$Choice, 1, 0))
	accuracy <- aggregate(results$isCorrect, by=list(results$WorkerId), mean, na.rm = T)
	disqualifiedWorkerIds <- subset(accuracy, x < 0.75)$WorkerId
	results <- subset(results, !(WorkerId %in% disqualifiedWorkerIds))

### Preliminary data analysis

An important first step is to visualize the data. This helps identify unexpected behavior in the course of the experiment or during the conversion of data to the correct format in the R script. It also gives you an understanding of the general patterns in the data and therefore of how the statistics should come out. We use the library `lattice` for visualization purposes in R. After it is installed, load it using the command `library(lattice)`. With this library, certain types of data like simple ratings and distribution of choices over a binary variable can be visualized for each condition by using the command: 

	histogram(~ Choice | Factor1 * Factor2, data=results)

A second useful step is to aggregate, or compute the mean of each Choice made by participants according to certain criteria. For example, the first line of code below will return a mean of the Choice by participant, and the second line will return a mean by participant and two factors. These results will help detect interesting patterns in the data.

	aggregate(results$Choice, by=list(results$WorkerId), mean)
	aggregate(results$Choice, by=list(results$WorkerId, results$Factor1, results$Factor2), mean)

The `analysis.r` script provided with *turktools* contains similar simple suggestions for dealing with completions data, which is somewhat different than forced-choice and Likert scale ratings. For additional suggestions for data visualization and basic analysis of linguistic grammaticality surveys using Likert scale ratings, see Gibson et al. (2011). Gibson et al’s discussion is also applicable to similar designs using a binary decision (e.g. ‘yes’-‘no’ or ‘natural’-‘unnatural’). See additionally the literature suggested there and in this paper for more detailed reading on the theory and implementation of more sophisticated statistical tests. 

### Dealing with unexpected results

After getting an impression of the results of your study and performing a statistical analysis, it is sometimes the case that the results are not exactly as had been expected prior to the experiment. This result can be due to many factors, not least of which is that the hypothesis that the predictions were based on is incorrect for the data used in the experiment. However, before an experiment can be used to contest existing theories and put forward new ones, it is important to check what other factors may have led to the unexpected results. 

As a first step, when filtering based on the accuracy of filler items or comprehension questions, it is important to make sure that the items are generally understood by participants as expected. For that purpose, it is useful to look at the mean accuracy for each item that had an expected value. See Section 11 for R code that can produce mean accuracy values per item. It is also useful to similarly treat target items: for all items that are expected to yield a certain result, aggregate the mean accuracy for those items and search for any exceptions that may be introducing noise into the analysis. It may be the case that certain items should be re-written and the experiment re-run, in order to avoid such effects of individual items.

Moreover, it is possible that there are different sub-groups of items that exhibit different patterns of judgments, only some of which were expected. In that case, we recommend trying to identify the factors that define these different groupings. Once this is done, the status of these grouping factors must be examined: it is possible that such factors should be considered relevant to the behavior at hand and hence added to the experiment as a factor that co-varies systematically with the other factors of interest. On the other hand, it is possible that the factor is not theoretically relevant, and in that case the noise should be controlled for by keeping just one kind of item as opposed to items that vary in their behavior with regard to this theoretically irrelevant factor. 

After looking at individual items, it is also important to look at the behavior of individual participants in the experiment to identify any unusual behavior. Participants who were not paying attention to the task should have already been excluded from the analysis by means of filler accuracy and comprehension questions. However, it is possible that participants who have not been excluded nonetheless performed poorly in one or more conditions, or after a certain point in the study. It may be possible that some participants should be excluded, despite meeting the basic accuracy criteria, for consistently performing poorly in certain cases in an idiosyncratic manner not common among other participants. To identify such subjects, it is helpful to examine the accuracy of target and filler items by participant, to detect any unusual pattern in the data. 

It is also possible that for some linguistic phenomena, participants who speak a second language behave differently than mono-lingual speakers. To test this possibility, we recommend comparing the results yielded by analyzing data from all native-speakers to data from only those speakers who reported that they are native speakers who do not speak any foreign language. This can be done as follows, using the value stored in the foreign column by our skeletons:

	results <- subset(results, foreign == 1)

Lastly, it may be helpful to split participants according to the speed with which they finished the study. For some tasks, it is reasonable to assume that participants who were very fast performed the task using a different strategy than slower participants. As a first step, it is possible to split the participant population by the average experiment completion time, classifying all participants who were faster than the mean as ‘fast’ and all the others as ‘slow.’ After this classification is done, for example using the code below, it is advisable to re-do the analysis that was previously performed on the entire population on each subgroup separately, to see whether there is variation among the groups.
 
	meanTime <- mean(targets$WorkTimeInSeconds)
	fastWorkers <- subset(targets, targets$WorkTimeInSeconds < MeanTime)
	slowWorkers <- subset(targets, targets$WorkTimeInSeconds >= MeanTime)

More generally, it is often advisable not to rely on the results of the initial version of an experiment. Rather, those initial results should be considered pilot data. This data should then be scrutinized, any items that did not yield expected results should be corrected, and the experiment should be re-run to confirm the original findings. It is often the case that after more consideration has been given to the data and analysis, the original results will change or be refined. 

### References: 
* Baayen, R. H. 2008. Analyzing linguistic data: a practical introduction to statistics using R. Cambridge, UK: Cambridge University Press. 
* Baayen, R.H., Davidson, D.J., Bates, D.M. 2008. Mixed-effects modeling with crossed random effects for subjects and items. Journal of Memory and Language, 59, 390-412.
* Bates, D.M. and Maechler, M. 2009. lme4: Linear mixed-effects models using S4 classes. R package version 0.999375-32.
* Barr, D.J., Levy, R., Scheepers, C., and Tily, H.J,. 2013. Random effects structure for confirm-atory hypothesis testing: Keep it maximal. Journal of Memory and Language 68(3):255-278.
* DeGroot, M. H., Schervish, M. J., Fang, X., Lu, L., and Li, D. 1986. Probability and statistics. Reading, MA: Addison-Wesley.
* Gelman, A., and Hill, J. 2007. Data analysis using regression and multilevel ⁄ hierarchical models. Cambridge, UK: Cambridge University Press.
* Gibson, E., Piantadosi, S., and Fedorenko, K. 2011. Using Mechanical Turk to Obtain and Analyze English Acceptability Judgments. Language and Linguistics Compass 5/8: 509–524.
