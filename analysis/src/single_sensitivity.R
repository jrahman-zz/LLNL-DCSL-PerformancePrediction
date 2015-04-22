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
test_data=read.csv(args[1],
			head=T,
			sep=',',
			stringsAsFactors=T)

# Get configuration information
# We don't want dummy inteference data here, since that is only for baseline
scrubbed = test_data[test_data$interference != 'dummy', ]
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
  median(abs(predict(model, data) - data$time) / data$time) * 100
}

boot.pred_mean = function(data, indices) {
    data = data[indices,]
    median(abs(data)) * 100
}

print('Loading models...')
load(args[2])
print('Loaded models')

# Plot results

# Create scatter plot of group variance v.s. prediction error
# Group by interference level, colocation level, and nice level

applications = c()
base.rmse = c()
pred.rmse = c()
models.rmse = c()
runs.rmse = c()

# Filter out any column except for our predictors and the response variable
drops = c('application', 'interference', 'coloc', 'cores', 'rep', 'nice')
run_counts = c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
for (run_count in run_counts) {
  model_set = models[[run_count]]
  for (app in names(model_set)) {
    print(paste("App: ", app))
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
          for (model in names(model_set[[app]])) {
            mod = model_set[[app]][[model]]
            pred = predict(mod, data)
            err.diff = (pred - data$time)
            err.abs = abs(err.diff)
            err.rmse = sqrt(mean(err.abs^2))
            err.rel = err.rmse / times.mean * 100
                    
            applications = c(applications, app)
            models.rmse = c(models.rmse, model)
            base.rmse = c(base.rmse, times.rel)
            pred.rmse = c(pred.rmse, err.rel)
            runs.rmse = c(runs.rmse, run_count)
          }
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


err.points = data.frame(application=applications, model=models.rmse, base_rmse=base.rmse, pred_rmse=pred.rmse, runs=runs.rmse)

# Plot the base RMSE vs. the prediction RMSE
pdf('prediction_sensitivity_rmse.pdf', width=11, height=8.5)

# Group by model first
xyplot(pred_rmse ~ base_rmse | runs,
       group=model,
       data=err.points,
       auto.key=list(space='right'),
       xlab="Mean Difference Normalized RMSE",
       ylab="Prediction Normalized RMSE",
       main="Prediction RMSE vs. Mean Difference RMSE",
       par.settings=plot.settings
    )

# Group by application
xyplot(pred_rmse ~ base_rmse | runs,
       group=application,
       data=err.points,
       auto.key=list(space='right'),
       xlab="Mean Difference Normalized RMSE", 
       ylab="Prediction Normalized RMSE",
       main="Prediction RMSE vs. Mean Difference RMSE",
       par.settings=plot.settings
    )

histogram(~pred_rmse | runs, data=err.points, group=model, xlab="Normalized Prediction RMSE")

dev.off()

# Generate prediction errors from the test set
applications = c()
models.used = c()
runs.used = c()
err = c()
upp = c()
low = c()
group = c()

print(run_counts)
i = 0
for (run_count in run_counts) {
  model_set = models[[run_count]]
  for (app in names(model_set)) {

    # Select all rows for our application
    test.set = test_data[test_data$application == app, ]
    test.set = test.set[test.set$interference != 'dummy', ]

    # Truncate columns that we do not want to be used in the fitting
    drops = c('application', 'interference', 'coloc', 'cores', 'rep', 'nice')
    test.data = test.set[, !(names(test.set) %in% drops)]

    for (model in names(model_set[[app]])) {
    
      fit = model_set[[app]][[model]]
      fit.boot = boot(data=test.data,
                      statistic=boot.pred,
                      R=250,
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
      runs.used = c(runs.used, run_count)
      group = c(group, i %% 5)
    }
    i = i + 1
  }
}

# Sort the rows of error based first on application then group by model
error = data.frame(application=applications,
                   model=models.used,
                   error=err,
                   low=low,
                   upp=upp,
                   group=group,
                   runs=runs.used)

error <- error[order(error$application, error$model),]

pdf("prediction_error_sensitivity.pdf", width=11, height=8.5)
for (group in unique(error$group)) {
    print(paste("Group: ", group))
    print(paste("Group size: ", length(error[error$group == group, ]$error)))
    p = barchart(error~application | runs,
                data=error[error$group==group, ],
                groups=model,
                auto.key = list(space = "right"),
                xlab='Median Prediction Error %',
                main='Prediction Error',
                border='white',
                par.settings=plot.settings)
    print(p)
}
dev.off()


# Print out final warnings as notification
warnings()
