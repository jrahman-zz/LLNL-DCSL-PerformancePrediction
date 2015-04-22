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
  median(abs(data$time - predict(model, data)) / data$time) * 100
}

boot.pred2 = function(data, indices, mean) {
    data=data[indices, ]
    median(data$time - mean) / data$time * 100
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
base.rmse = c()
pred.rmse = c()
models.rmse = c()
coloc.rmse = c()
interfere.rmse = c()
rel.rmse = c()

# Filter out any column except for our predictors and the response variable
drops = c('application', 'interference', 'cores', 'coloc', 'rep', 'nice')
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
                times.abs = abs(times - times.mean)
                times.rmse = sqrt(mean(times.abs^2))
                times.rel = times.rmse / times.mean * 100
                
                # Compute the error for each model, 
                for (model in names(models[[app]])) {
                  mod = models[[app]][[model]]
                  pred = predict(mod, data)
                  err.diff = (data$time - pred)
                  err.abs = abs(err.diff)
                  err.rmse = sqrt(mean(err.abs^2))
                  err.rel = err.rmse / times.mean * 100
                    
                  applications = c(applications, app)
                  models.rmse = c(models.rmse, model)
                  coloc.rmse = c(coloc.rmse, coloc_level)
                  interfere.rmse = c(interfere.rmse, interfere)
                  base.rmse = c(base.rmse, times.rel)
                  pred.rmse = c(pred.rmse, err.rel)
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


err.points = data.frame(application=applications, model=models.rmse, base_rmse=base.rmse, pred_rmse=pred.rmse)

# Plot the base RMSE vs. the prediction RMSE
pdf('single_prediction_rmse.pdf', width=11, height=8.5)

# Group by model first
xyplot(pred_rmse ~ base_rmse,
       group=model,
       data=err.points,
       auto.key=list(space='right'),
       xlab="Mean Difference Normalized RMSE",
       ylab="Prediction Normalized RMSE",
       main="Prediction RMSE vs. Mean Difference RMSE",
       par.settings=plot.settings
    )

# Group by application
xyplot(pred_rmse ~ base_rmse,
       group=application,
       data=err.points,
       auto.key=list(space='right'),
       xlab="Mean Difference Normalized RMSE", 
       ylab="Prediction Normalized RMSE",
       main="Prediction RMSE vs. Mean Difference RMSE",
       par.settings=plot.settings
    )

histogram(~pred_rmse | model, data=err.points, group=model, xlab="Normalized Prediction RMSE")
dev.off()

# Print list of errors above 10%
print(err.points[err.points$pred_rmse > 10, ])

warnings()
