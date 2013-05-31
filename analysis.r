#####################################################################################
##    Sample analysis script for linguistic surveys run on Mechanical Turk         ##
##    For surveys cosntructed using the tools described in Erlewine&Kotek (2013)   ##
##    May 2013 Hadas Kotek, licensed under the MIT license                         ##
#####################################################################################

# file prep ----

# read in the file
results <- read.csv("xxxxxxxxxxxxxx.decoded.csv",header=TRUE) 

# reject non-native speakers
results <- subset(results, english == 1)

# reject non mono-lingual speakers?
#results <- subset(results, foreign == 1)


# reject participants who completed more than one survey or did not finish the survey
# mark unanswered questions with 0, all answered questions with 1
results$isNA <- ifelse(is.na(results$Choice) | results$Choice == '', 0, 1)

# count how many questions were answered by each participant
howMany <- aggregate(results$isNA, list(results$WorkerId), sum)

# compute the length of a survey in your study
SurveyLength <- as.numeric(aggregate(results$AssignmentId, by=list(results$AssignmentId), length)$x[1])

# set the completion rate below which submissions should be rejected
NotEnough <- 0.8*SurveyLength

# compute how many participants answered too many surveys or not enough questions in the survey
didTooMany <- subset(howMany, x > SurveyLength)$Group.1
didntDoEnough <- subset(howMany, x < NotEnough)$Group.1

# remove these participants from the analysis
results <- subset(results, !(WorkerId %in% didTooMany))
results <- subset(results, !(WorkerId %in% didntDoEnough))


# reject participants with low accuracy. ----
# compute accuracy for any question that had expected values such as filler items, comprehension questions and filler items
# here: we assume that the correct response to the item was saved in a hidden field, field_5 
# the field number should be modified according to its number in your items file
results$isCorrect <- ifelse(is.na(results$field_5), NA, ifelse(results$field_5 == results$Choice, 1, 0))
Accuracy <- aggregate(results$isCorrect, by=list(results$WorkerId), mean, na.rm = T)
lowAcc <- subset(Accuracy, x < 0.75)$WorkerId
results <- subset(results, !(WorkerId %in% lowAcc))


# create a dataframe for target items ---
# here, assuming all non-fillers are target sections
targets <- subset(results, results$Section != 'filler')

#remane factors, give columns meaningful names
#code below assumes two factors, change as needed
library(plyr)
targets <- rename(targets, c("Factor1"="XXXX", "Factor2"="YYYY"))


# data visualization ----
# plot histograms by the different factors in your experiment for each condition
library(lattice)
histogram(~ Choice | Factor1 * Factor2, data=targets)
histogram(~ Choice | Factor1, data=targets)
histogram(~ Choice | Factor2, data=targets)
histogram(~ Choice, data=targets)


# basic aggregation (for ratings or binary forced choice coded as 0-1)----
aggregate(targets$Choice, by=list(targets$WorkerId), mean)
aggregate(targets$Choice, by=list(targets$WorkerId, targets$Factor1, targets$Factor2), mean)

# basic aggregation (for completions)
aggregate(targets$WorkerId, by=list(targets$Choice), length)
aggregate(targets$WorkerId, by=list(targets$Choice, targets$Factor1, targets$Factor2), length)


# looking at individual items ----
#target items (for ratings or binary forced choice coded as 0-1)
aggregate(targets$Choice, by=list(targets$Item), mean)
aggregate(targets$Choice, by=list(targets$Condition, targets$Item), mean)

# target items (for completions)
aggregate(targets$WorkerId, by=list(targets$Choice, targets$Condition), length)

# filler items with expected answers
aggregate(results$isCorrect, by=list(results$Item), mean, na.rm = T)

# slow vs. fast workers
# perform analysis separately on these groups instead of on all of targets.
meanTime <- mean(targets$WorkTimeInSeconds)
fastWorkers <- subset(targets, targets$WorkTimeInSeconds < MeanTime)
slowWorkers <- subset(targets, targets$WorkTimeInSeconds >= MeanTime)
