#!/usr/bin/Rscript

library(gbm)
library(MASS)
library(lars)
library(pls)
library(glmnet)
library(genalg)
library(foreach)
library(caret)

library(RColorBrewer)
library(lattice)

# Use parallelism
library(doMC)
registerDoMC(4)

#
# Perform analysis on training data set
# PCA for correlation between predictors
#

args = commandArgs(trailingOnly=TRUE)

# Read in data
train_data=read.csv(args[1],
                    head=T,
                    sep=',',
                    stringsAsFactors=T)

test_data=read.csv(args[2],
                   head=T,
                   sep=',',
                   stringsAsFactors=T)

# Get configuration information
# We don't want dummy inteference data here, since that is only for baseline
scrubbed = train_data[train_data$interference != 'dummy', ]
application.names   = unique(scrubbed$application)
interference.names  = unique(scrubbed$interference)
reps.indices        = unique(scrubbed$rep)
coloc.levels        = unique(scrubbed$coloc)
nice.levels         = unique(scrubbed$nice)

interference.test.names = unique(test_data[test_data$interference != 'dummy', ]$interference)

configs.data=list()
configs.count=0
# Plot clusters
#pdf('single_application_', width=10, height=5)
#par(mfrow=c(length(interference.names), 5))
#for (interfere in interference.names) {
#   boxplot()
#   boxplot()
#   boxplot()
#   boxplot()
#   boxplot()
#}
#dev.off()

# Remove non-benchmark columns
drops = c('application', 'interference', 'coloc', 'rep', 'nice', 'time')
predictors.data = train_data[train_data$interference != 'dummy', !(names(train_data) %in% drops)]
predictors.names = colnames(predictors.data)

predictors.pca <- prcomp(predictors.data,
                         center = TRUE,
                         scale = TRUE)

print(predictors.pca)
plot(predictors.pca, type = "l")
summary(predictors.pca)

predictors.pca <- prcomp(predictors.data,
                         center = FALSE,
                         scale = FALSE)

print(predictors.pca)
plot(predictors.pca, type="l")
summary(predictors.pca)

