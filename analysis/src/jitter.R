#!/usr/bin/Rscript

library(Hmisc)
library(rpart)
library(boot)
library(e1071)
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

args = commandArgs(trailingOnly=TRUE)

# Perform single application prediction
#
# Take a set of feature benchmarks along with application runtimes
# and create a model of the application runtime as a function of the
# feature benchmarks
#


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
application.names 	= unique(scrubbed$application)
interference.names 	= unique(scrubbed$interference)
reps.indices		= unique(scrubbed$rep)
coloc.levels		= unique(scrubbed$coloc)
nice.levels			= unique(scrubbed$nice)

interference.test.names = unique(test_data[test_data$interference != 'dummy', ]$interference)

drops = c('application', 'interference', 'cores', 'coloc', 'rep', 'nice', 'time')
predictors.data = train_data[train_data$interference != 'dummy', !(names(train_data) %in% drops)]
predictors.names = colnames(predictors.data)

# Check for runtime stability, no point in predicting a moving target
max_app_jitter = 0
max_bmark_jitter = 0
bmark_jitter_values = c()
bmark_dev_values = c()
app_jitter_values = c()
app_dev_values = c()
for (interfere in interference.names) {
    interference.data = train_data[train_data$interference == interfere, ]
	for (coloc_level in coloc.levels) {
        colocation.data = interference.data[interference.data$coloc == coloc_level, ]
		for (nice_level in nice.levels) {
            data = colocation.data[colocation.data$nice == nice_level, ]
    		print(interfere)

			for (name in predictors.names) {
				d = data[,name]
				if (length(d) > 0) {
					minimum = min(d)
					maximum = max(d)
					mean = mean(d)
                    s = sd(d)
					jitter = (maximum-minimum)/mean
                    dev = s/mean
                    bmark_dev_values = c(bmark_dev_values, dev)
					bmark_jitter_values = c(bmark_jitter_values, jitter)
					max_bmark_jitter = max(max_bmark_jitter, jitter)
				}
			}	
			for (app in application.names) {
				d = data[data$application==app,'time']
				if (length(d) > 0) {
					minimum = min(d)
					maximum = max(d)
					mean = mean(d)
                    s= sd(d)
                    dev = s/mean
					jitter = (maximum-minimum)/mean
                    app_dev_values = c(app_dev_values, dev)
					app_jitter_values = c(app_jitter_values, jitter)
					max_app_jitter = max(max_app_jitter, jitter)
				}
			}
		}
	}
}
print(paste("App: ", max_app_jitter, ", Bmark: ", max_bmark_jitter))
pdf(paste(args[4], '_jitter.pdf'), height=8.5, width=11)
hist(app_dev_values, breaks=10, xlab="sd/mean", main="App runtime coefficient of variation")
hist(bmark_dev_values, breaks=10, xlab="sd/mean", main="Benchmark runtime coefficient of variation")
hist(app_jitter_values, breaks=10, xlab="(max-min)/mean", main="App runtime jitter")
hist(bmark_jitter_values, breaks=10, xlab="(max-min)/mean", main="Benchmark runtime jitter")
dev.off()

warnings()
