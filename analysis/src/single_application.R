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
#library(caret)

# Use parallelism
library(doMC)
registerDoMC(8)


# Perform single application prediction
#
# Take a set of feature benchmarks along with application runtimes
# and create a model of the application runtime as a function of the
# feature benchmarks
#


error.bar <- function(x, y, upper, lower=upper, length=0.1,...){
  if(length(x) != length(y) | length(y) !=length(lower) | length(lower) != length(upper))
    stop("vectors must be same length")
  arrows(x,y+upper, x, y-lower, angle=90, code=3, length=length, ...)
}

# Read in data
train_data=read.csv('../data/train_single_sierra.csv',
			head=T,
			sep=',',
			stringsAsFactors=T)

test_data=read.csv('../data/test1_single_sierra.csv',
			head=T,
			sep=',',
			stringsAsFactors=T)

# Get configuration information
application.names 	= unique(train_data$application)
interference.names 	= unique(train_data$interference)
reps.indices		= unique(train_data$rep)
coloc.levels		= unique(train_data$coloc)
nice.levels			= unique(train_data$nice)


configs.data=list()
configs.count=0
# Look at clustering within a given interference config
#for (interfere in interference.names) {
#	for (level in coloc.levels) {
#		for (nice in nice.levels) {
#			data = train_data[train_data$interference == interfere,]
#			data = data[data$coloc == level,]
#			data = data[data$nice == nice,]
#			if (length(data) > 0) {
#				configs.count = configs.count + 1
#			}
#			configs.data[[interfere]][[level]][[nice]] = data
#		}
#	}
#}

# Plot clusters
#pdf('single_application_', width=10, height=5)
#par(mfrow=c(length(interference.names), 5))
#for (interfere in interference.names) {
#	boxplot()
#	boxplot()
#	boxplot()
#	boxplot()
#	boxplot()
#}
#dev.off()

# Remove non-benchmark columns
drops = c('application', 'interference', 'coloc', 'rep', 'nice', 'time')
predictors = train_data[, !(names(train_data) %in% drops)]

length(predictors[,1])

predictors.pca <- prcomp(predictors,
						center = TRUE,
						scale = TRUE)

print(predictors.pca)
plot(predictors.pca, type = "l")
summary(predictors.pca)

predictors.pca <- prcomp(predictors,
						center = FALSE,
						scale = FALSE)

print(predictors.pca)
plot(predictors.pca, type="l")
summary(predictors.pca)

pdf("app_times.pdf", width=11.5, height=8)
#par(mfrow=c(length(application.names), 5), xpd=T)
for (app in application.names) {
	#data = train_data[train_data$application == app,]
	#l0 = data[data$coloc == 0,]
	#l1 = data[data$coloc == 1,]
	#l2 = data[data$coloc == 2,]
	#d = l0[l0$nice == 0,]
	#plot(, )
	#plot()
	#plot()
	#plot()
	#plot()
	data = train_data[train_data$application == app,]
	l0 = data[data$coloc == 0,]
	l1 = data[data$coloc == 1,]
	l2 = data[data$coloc == 2,]

	print(paste("App: ", app))
	print(paste("Coloc 0: ", length(l0$time)))
	print(paste("Coloc 1: ", length(l1$time)))
	print(paste("Coloc 2: ", length(l2$time)))

	print(l1$time)
	print(l2$time)

	minimum = min(data$time)
	maximum = max(data$time)
	lim = c(minimum, maximum)

	caption = paste("Runtimes: ", app)
	stripchart(l0[l0$nice==0,]$time, method="jitter", main=caption, col="red", xlim=lim)
	stripchart(l0[l0$nice==5,]$time, method="jitter", main="", col="orange", xlim=lim, add=TRUE)
	stripchart(l2$time, method="jitter", main="", col="green", xlim=lim, add=TRUE)
	stripchart(l0[l0$nice==10,]$time, method="jitter", main="", col="yellow", xlim=lim, add=TRUE)
	stripchart(l1$time, method="jitter", main="", col="blue", xlim=lim, add=TRUE)
	legend("topleft", legend=c("Same core, nice 0", "Same core, nice 5", "Same core, nice 10", "Same socket, different core", "Different socket"), text.col=c("red", "orange", "yellow", "blue", "green"))
}
dev.off()

# Compute training error
compute.error = function(y0, y1) {
  abs(y1-y0)/y0
}

boot.pred=function(data, indices, model) {
  # Compute the mean error statistic for boot strapping
  #
  # Args:
  #   data:
  #   indices: Bootstrap method chooses indices
  #   model: Trained model to run data through
  #
  data=data[indices, ]
  median(abs(predict(model, data) - data$y) / data$y) * 100
}

model.names = c("lm", "svmRadial", "gbm")

# Define our formula for y in terms of others
formula=as.formula('time~.')

ci=list()

# Build models and use test set for error analysis
for (application in application.names) %dopar% {
  
  # Select all rows for our application
  training.set = train_data[train_data$application == application, ]
  test.set = test_data[test_data$application == application, ]

  print(application)
  
  # Truncate columns that we do not want to be used in the fitting
  drops = c('application', 'interference', 'coloc', 'rep', 'nice')
  training.data = training.set[, !(names(training.set) %in% drops)]
  testing.data = test.set[, !(names(test.set) %in% drops)]
 
  # Sweep over models
  for (model in model.names) %dopar% {
    
    control.object=trainControl(
						method='repeatedcv',
						repeats=5,
						number=10,
						preProcOptions=list(method=c("Box-Cox", "center", "scale"))
					)
    set.seed(1)
    
    # Create a fit mapping from features (no interference) to application performance
    fit=train(form = train ~ ., data=training.data, method=model, trControl=control.object)
    
    fit.boot=boot(data=testing.data, statistic=boot.pred, R=999, model=fit)
    # see for bca: "Better Bootstrap Confidence Intervals" by Efron 1987.
    # see "Bootstrapping Regression Models" by John Fox 2002.  
    ci[[application]][[model]]=boot.ci(fit.boot, type="bca")
  }
}

# Plot results
pdf("predict_application_clean_environment.pdf", width=11, height=8.5)
par(mar=c(10,4,1,0), xpd=T)
err=sapply(ci, function(x) x[[1]]$t0)
low=sapply(ci, function(x) x[[1]]$bca[4])
upp=sapply(ci, function(x) x[[1]]$bca[5])
bars = barplot(err,
               beside=T, las=3, cex.names=0.8,
               ylim=c(0, extendrange(c(err, upp, low))[2]),
               ylab='Median Prediction Error %',
               col="green", border='white')
error.bar(bars, err, upp-err, err-low)
text(bars, 0, round(err, 1), srt=90, adj=c(0,0.5), cex=0.8)
dev.off()
