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


error.bar <- function(x, y, upper, lower=upper, length=0.1,...){
  if(length(x) != length(y) | length(y) !=length(lower) | length(lower) != length(upper))
    stop("vectors must be same length")
  arrows(x,y+upper, x, y-lower, angle=90, code=3, length=length, ...)
}

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
drops = c('application', 'interference', 'coloc', 'rep', 'nice', 'time')
predictors.data = train_data[train_data$interference != 'dummy', !(names(train_data) %in% drops)]
predictors.names = colnames(predictors.data)

pdf("app_times.pdf", width=11.5, height=8)
#par(mfrow=c(length(application.names), 5), xpd=T)
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
#					if (jitter > 0.15) {
#						print(paste("Benchmark: ", name))
#						print(paste("Interference: ", interfere))
#						print(paste("Coloc: ", coloc_level))
#						print(paste("Nice: ", nice_level))
#						print(paste("Measurements: ", length(d)))
#						print(paste("Jitter: ", jitter))
#					}
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
#    				if (jitter > 0.15) {
#						print(paste("Application: ", app))
#						print(paste("Interference: ", interfere))
#						print(paste("Coloc: ", coloc_level))
#						print(paste("Nice: ", nice_level))
#						print(paste("Measurements: ", length(d)))
#						print(paste("Jitter: ", jitter))
#					}	
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


for (app in application.names) {
  # Compute the error assuming the mean is our prediction
  # Effectively determine the natural variance of the data
  training.data = train_data[train_data$application == app, ]
  training.data = training.data[training.data$interference == 'dummy', ]
  accum = c()
  times = training.data[,'time']
  m = mean(times)
  for (time in times) {
    diff = (time - m) / time
    accum = c(accum, diff)
  }
  print(paste("App: ", app, ", baseline sd: ", sd(accum)))
}

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
  median(abs(predict(model, data) - data$time) / data$time) * 100
}

boot.pred_mean = function(data, indices) {
    data = data[indices,]
    median(abs(data)) * 100
}

print('Loading models...')
load(args[3])
print('Loaded models')

# Plot results

# Create scatter plot of group variance v.s. prediction error
# Group by interference level, colocation level, and nice level

applications = c()
base_rmse = c()
pred_rmse = c()
models.used = c()

# Filter out any column except for our predictors and the response variable
drops = c('application', 'interference', 'coloc', 'rep', 'nice')
for (app in names(models)) {
    print(app)
    application.data = test_data[test_data$application == app, ]
    for (interfere in interference.test.names) {
        interference.data = application.data[application.data$interference == interfere, ]
	    for (coloc_level in coloc.levels) {
            colocation.data = interference.data[interference.data$coloc == coloc_level, ]
		    for (nice_level in nice.levels) {
                data = colocation.data[colocation.data$nice == nice_level, ]
                data = data[ ,!(names(data) %in% drops)]
                
                times = data$time

                # Grab the mean as the baseline
                times.mean = mean(times)
                times.abs = times - times.mean
                times.rel = times.abs / times
                times.sd = sd(times.rel)

                # Compute the error for each model, 
                for (model in names(models[[app]])) {
                    mod = models[[app]][[model]]
                    print(paste("Model: ", model, ", app: ", app))
                    pred = predict(mod, data)
                    err.diff = (data$time - pred)
                    err.abs = abs(err.diff)
                    err.rel = err.abs / data$time
                    print(err.abs)
                    print(err.rel)
                    err.sd = sd(err.rel)
                    applications = c(applications, app)
                    models.used = c(models.used, model)
                    base_rmse = c(base_rmse, times.sd)
                    pred_rmse = c(pred_rmse, err.sd)
                }
            }
        }
    }
}

# Prepare plot configuration
colors <- brewer.pal(6,"Blues")
plot.settings <- list(
  superpose.polygon=list(col=colors[2:5], border="transparent"),
  strip.background=list(col=colors[6]),
  strip.border=list(col="black")
)


err.points = data.frame(application=applications, model=models.used, base_rmse=base_rmse, pred_rmse=pred_rmse)

# Plot the base RMSE vs. the prediction RMSE
pdf('base_pred_rmse.pdf', width=11, height=8.5)

# Group by model first
xyplot(pred_rmse ~ base_rmse,
       group=model,
       data=err.points,
       auto.key=list(space='right'),
       xlab="Mean RMSE",
       ylab="Prediction RMSE",
       main="Prediction RMSE v.s. Runtime RMSE",
       par.settings=plot.settings
    )

# Group by application
xyplot(pred_rmse ~ base_rmse,
       group=application,
       data=err.points,
       auto.key=list(space='right'),
       xlab="Mean RMSE",
       ylab="Prediction RMSE",
       main="Prediciton RMSE vs. Runtime RMSE",
       par.settings=plot.settings
    )
dev.off()

#range = extendrange(c(error$error, error$upp, error$low))[2]

# Split data into four sets
#i = 0
#sets = split(application.names, cut(seq_along(application.names), 2, labels=FALSE))
#print("Sets")
#print(sets)

# Generate prediction errors from the test set
applications = c()
models.used = c()
err = c()
upp = c()
low = c()
for (app in names(models)) {
    
  # Select all rows for our application
  training.set = train_data[train_data$application == app, ]
  test.set = test_data[test_data$application == app, ]

  training.set = training.set[training.set$interference != 'dummy', ]
  test.set = test.set[test.set$interference != 'dummy', ]

  # Truncate columns that we do not want to be used in the fitting
  drops = c('application', 'interference', 'coloc', 'rep', 'nice')
  training.data = training.set[, !(names(training.set) %in% drops)]
  test.data = test.set[, !(names(test.set) %in% drops)]

  for (model in names(models[[app]])) {
    
    fit = models[[app]][[model]]
    fit.boot = boot(data=test.data,
                    statistic=boot.pred,
                    R=999,
                    model=fit,
                    parallel=c('multicore'),
                    ncpus=4)

    # see for bca: "Better Bootstrap Confidence Intervals" by Efron 1987.
    # see "Bootstrapping Regression Models" by John Fox 2002.  
    bootstrap = boot.ci(fit.boot, type='bca')
    err = c(err, bootstrap$t0)
    low = c(low, bootstrap$bca[4])
    upp = c(upp, bootstrap$bca[5])
    applications = c(applications, app)
    models.used = c(models.used, model)
  }
}

# Sort the rows of error based first on application then group by model
error = data.frame(application=applications,
                   model=models.used,
                   error=err,
                   low=low,
                   upp=upp)

error <- error[order(error$application, error$model),]

pdf("prediction_single_application.pdf", width=11, height=8.5)
barchart(error~application,
                data=error,
                groups=model,
                auto.key = list(space = "right"),
                xlab='Median Prediction Error %',
                main='Prediction Error',
                border='white',
                par.settings=plot.settings)
dev.off()

#for (i in (1:length(sets))) {
#  print(i)
#  set = sets[[i]]
#  print(set)
#  plot.data = data.frame()
#  for (app in set) {
#    plot.data = rbind(plot.data, error[error$application == app, ])
#  }
#
#  pdf(paste("predict_application_", i, ".pdf"), width=11, height=8.5)`
#  par(mar=c(10,4,1,0), xpd=T)
#
#  print(set)
#  print(plot.data$error)
##  barchart(error~application,
#                data=plot.data,
#                groups=model,
#                auto.key = list(space = "right"),
#                xlab='Median Prediction Error %',
#                main='Prediction Error',
#                border='white',
#                par.settings=plot.setting)
  flush.console()
#  dev.off()
#}
#error.bar(bars, error$error, error$upp-error$error, error$error-error$low)
#text(bars, 0, round(err, 1), srt=90, adj=c(0,0.5), cex=0.8)

# Print out final warnings as notification
warnings()
