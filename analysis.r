################################################################################
## Sample analysis script for linguistic surveys run on Mechanical Turk       ##
## For surveys cosntructed using the tools described in Erlewine&Kotek (2013) ##
## May 2013 Hadas Kotek, licensed under the MIT license                       ## 
################################################################################


# file prep ----

# read in the file
results <- read.csv("xxxxxxxxxxxxxx.decoded.csv",header=TRUE) 

# reject non-native speakers
results <- subset(results, english == 1)


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
compAccuracy <- aggregate(results$isCorrect, list(WorkerId = results$WorkerId), mean, na.rm = T)
lowAcc <- subset(compAccuracy, x < 0.75)$WorkerId
results <- subset(results, !(WorkerId %in% lowAcc))


# extract factor values out of the condition names and store them in separate columns ----
# replace Factor1, Factor2, Factor3 etc.. with meaningful names based on the experiment
results$Factor1 <- sub("^(.*)-(.*)-(.*)$", "\\1", results$Condition)
results$Factor2 <- sub("^(.*)-(.*)-(.*)$", "\\2", results$Condition)
results$Factor3 <- sub("^(.*)-(.*)-(.*)$", "\\3", results$Condition)

# data visualization ----
# plot histograms by the different factors in your experiment for each condition
library(lattice)
histogram(~ Choice | Factor1 * Factor2, data=results)
histogram(~ Choice | Factor1, data=results)
histogram(~ Choice | Factor2, data=results)
histogram(~ Choice, data=results)

# basic aggregation ----
aggregate(results$Choice, by=list(results$WorkerId), mean)
aggregate(results$Choice, by=list(results$WorkerId, results$Factor1, results$Factor2), mean)

