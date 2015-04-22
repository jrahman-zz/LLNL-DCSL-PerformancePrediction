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

# Prepare plot configuration
colors <- brewer.pal(6,"Blues")
plot.settings <- list(
  superpose.polygon=list(col=colors[2:5], border="transparent"),
  strip.background=list(col=colors[6]),
  strip.border=list(col="black")
)

# Generate prediction errors from the test set
applications = c()
models.used = c()
err = c()
upp = c()
low = c()
group = c()

i = 0
for (app in names(models)) {

  # Select all rows for our application
  test.set = test_data[test_data$application == app, ]
  test.set = test.set[test.set$interference != 'dummy', ]

  # Truncate columns that we do not want to be used in the fitting
  drops = c('application', 'interference', 'coloc', 'cores', 'rep', 'nice')
  test.data = test.set[, !(names(test.set) %in% drops)]

  for (model in names(models[[app]])) {
    
    fit = models[[app]][[model]]
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
    group = c(group, i %% 5)
  }

  # Terrible naive mean model
  data = train_data[train_data$application == app, ]
  data = data[, !(names(data) %in% drops)]
  m = mean(data$time)
  fit.boot = boot(data=data,
                  statistic=boot.pred2,
                  R=250,
                  mean=m,
                  parallel=c('multicore'),
                  ncpus=4)

  bootstrap = boot.ci(fit.boot, type='bca')
  applications = c(applications, app)
  models.used = c(models.used, 'Naive Mean')
  group = c(group, i %% 5)
  err = c(err, bootstrap$t0)
  low = c(low, bootstrap$bca[4])
  upp = c(upp, bootstrap$bca[5])

  i = i + 1
}

# Sort the rows of error based first on application then group by model
error = data.frame(application=applications,
                   model=models.used,
                   error=err,
                   low=low,
                   upp=upp,
                   group=group)

error <- error[order(error$application, error$model),]

pdf("prediction_error.pdf", width=11, height=8.5)
for (group in unique(error$group)) {
    print(paste("Group: ", group))
    print(paste("Group size: ", length(error[error$group == group, ]$error)))
    p = barchart(error~application,
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

warnings()
