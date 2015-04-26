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

# Remove non-benchmark columns
drops = c('application', 'interference', 'cores', 'coloc', 'rep', 'nice', 'time')
predictors.data = train_data[train_data$interference != 'dummy', !(names(train_data) %in% drops)]
predictors.names = colnames(predictors.data)

pdf(paste(args[4], '_application_times.pdf'), width=11.5, height=8)
for (app in application.names) {
	data = train_data[train_data$application == app, ]
    dummy= data[data$interference == 'dummy', ]
	l0 = data[data$coloc == 0, ]
    l0 = l0[l0$interference != 'dummy', ]
	l1 = data[data$coloc == 1, ]
	l2 = data[data$coloc == 2, ]

	minimum = min(data$time)
	maximum = max(data$time)
	lim = c(minimum, maximum)

	caption = paste("Runtimes: ", app)
	stripchart(l0[l0$nice==0,]$time, method="jitter", main=caption, col="red", xlim=lim)
	stripchart(l0[l0$nice==5,]$time, method="jitter", main="", col="orange", xlim=lim, add=TRUE)
	stripchart(l0[l0$nice==10,]$time, method="jitter", main="", col="yellow", xlim=lim, add=TRUE)
	stripchart(l1$time, method="jitter", main="", col="blue", xlim=lim, add=TRUE)
	stripchart(l2$time, method="jitter", main="", col="green", xlim=lim, add=TRUE)
    stripchart(dummy$time, method="jitter", main="", col="purple", xlim=lim, add=TRUE)
	legend("topleft", legend=c("Same core, nice 0", "Same core, nice 5", "Same core, nice 10", "Same socket, different core", "Different socket", "Baseline"), text.col=c("red", "orange", "yellow", "blue", "green", "purple"))
}
dev.off()

warnings()
