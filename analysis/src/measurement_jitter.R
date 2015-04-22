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

# Remove non-benchmark columns
drops = c('application', 'interference', 'cores', 'coloc', 'rep', 'nice', 'time')
predictors.data = train_data[train_data$interference != 'dummy', !(names(train_data) %in% drops)]
predictors.names = colnames(predictors.data)

pdf("application_times.pdf", width=11.5, height=8)
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
pdf('jitter.pdf', height=8.5, width=11)
hist(app_dev_values, breaks=10, xlab="sd/mean", main="App runtime coefficient of variation")
hist(bmark_dev_values, breaks=10, xlab="sd/mean", main="Benchmark runtime coefficient of variation")
hist(app_jitter_values, breaks=10, xlab="(max-min)/mean", main="App runtime jitter")
hist(bmark_jitter_values, breaks=10, xlab="(max-min)/mean", main="Benchmark runtime jitter")
dev.off()

warnings()
