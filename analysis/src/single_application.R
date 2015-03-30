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
#library(caret)

# Use parallelism
library(doMC)
registerDoMC(8)

args = commandArgs(trailingOnly=TRUE)

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
train_data=read.csv(args[1],
			head=T,
			sep=',',
			stringsAsFactors=F)

test_data=read.csv(args[2],
			head=T,
			sep=',',
			stringsAsFactors=F)

# Get configuration information
application.names 	= unique(train_data$application)
interference.names 	= unique(train_data$interference)
reps.indices		= unique(train_data$rep)
coloc.levels		= unique(train_data$coloc)
nice.levels			= unique(train_data$nice)


configs.data=list()
configs.count=0
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
predictors.data = train_data[, !(names(train_data) %in% drops)]
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

pdf("app_times.pdf", width=11.5, height=8)
#par(mfrow=c(length(application.names), 5), xpd=T)
for (app in application.names) {
	data = train_data[train_data$application == app,]
	l0 = data[data$coloc == 0,]
	l1 = data[data$coloc == 1,]
	l2 = data[data$coloc == 2,]

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

# Check for runtime stability, no point in predicting a moving target
max_app_jitter = 0
max_bmark_jitter = 0
bmark_jitter_values = c()
app_jitter_values = c()
for (interfere in interference.names) {
	for (coloc_level in coloc.levels) {
		for (nice_level in nice.levels) {
			print(interfere)
			data = train_data
			data = data[data$interference == interfere,]
			data = data[data$coloc == coloc_level,]
			data = data[data$nice == nice_level,]
	
			for (name in predictors.names) {
				d = data[,name]
				if (length(d) > 0) {
					minimum = min(d)
					maximum = max(d)
					mean = mean(d)
					jitter = (maximum-minimum)/mean
					bmark_jitter_values = c(bmark_jitter_values, jitter)
					max_bmark_jitter = max(max_bmark_jitter, jitter)
					if (jitter > 1) {
						print(paste("Benchmark: ", name))
						print(paste("Interference: ", interfere))
						print(paste("Coloc: ", coloc_level))
						print(paste("Nice: ", nice_level))
						print(paste("Measurements: ", length(d)))
						print(paste("Jitter: ", jitter))
					}
				}
			}	
			for (app in application.names) {
				d = data[data$application==app,'time']
				if (length(d) > 0) {
					minimum = min(d)
					maximum = max(d)
					mean = mean(d)
					jitter = (maximum-minimum)/mean
					app_jitter_values = c(app_jitter_values, jitter)
					max_app_jitter = max(max_app_jitter, jitter)
					if (jitter > 1) {
						print(paste("Application: ", app))
						print(paste("Interference: ", interfere))
						print(paste("Coloc: ", coloc_level))
						print(paste("Nice: ", nice_level))
						print(paste("Measurements: ", length(d)))
						print(paste("Jitter: ", jitter))
					}	
				}
			}
		}
	}
}
print(paste("App: ", max_app_jitter, ", Bmark: ", max_bmark_jitter))
pdf('jitter.pdf', height=8.5, width=11)
hist(app_jitter_values, breaks=10, xlab="(max-min)/mean", main="App runtime jitter")
hist(bmark_jitter_values, breaks=10, xlab="(max-min)/mean", main="Benchmark runtime jitter")
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
foreach (application = application.names) %dopar% {
  
  # Select all rows for our application
  training.set = train_data[train_data$application == application, ]
  test.set = test_data[test_data$application == application, ]

  # Truncate columns that we do not want to be used in the fitting
  drops = c('application', 'interference', 'coloc', 'rep', 'nice')
  training.data = training.set[, !(names(training.set) %in% drops)]
  testing.data = test.set[, !(names(test.set) %in% drops)]
 
  # Sweep over models
  foreach (model = model.names) %dopar% {
    
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
