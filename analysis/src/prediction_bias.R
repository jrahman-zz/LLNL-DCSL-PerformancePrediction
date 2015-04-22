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

application.skew = c()
model.skew = c()
coloc.skew = c()
interfere.skew = c()
err.skew = c()

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
                
                # Compute the error for each model, 
                for (model in names(models[[app]])) {
                  mod = models[[app]][[model]]
                  pred = predict(mod, data)
                  err.diff = (data$time - pred)

                  for (err in err.diff) {
                    application.skew = c(application.skew, app)
                    model.skew = c(model.skew, model)
                    coloc.skew = c(coloc.skew, coloc_level)
                    interfere.skew = c(interfere.skew, interfere)
                    err.skew = c(err.skew, err / times.mean * 100)
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

pdf('error_skew.pdf', width=11, height=8.5)

skew.points = data.frame(application=application.skew, model=model.skew, err=err.skew, coloc=coloc.skew, interfere=interfere.skew)

upp=max(err.skew)
low=min(err.skew)
breaks = seq(from=low-1,to=upp+1,by=1)
histogram(~err | model, data=skew.points, group=application, breaks=breaks, xlab="Normalized Prediction Error")

histogram(~err | application, data=skew.points, group=model, breaks=breaks, xlab="Normalized Prediction Error")

histogram(~err | interfere, data=skew.points, group=application, breaks=breaks, xlab="Normalized Prediction Error")

for (app in unique(skew.points$application)) {
  p = histogram(~err | model, data=skew.points[skew.points$application == app, ], group=model, xlab=paste("Normalized Prediction Error - ", app))
  print(p)
}

dev.off()

warnings()
