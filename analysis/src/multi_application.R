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

# Get configuration informationi
# We don't want dummy inteference data here, since that is only for baseline
scrubbed = train_data[train_data$interference != 'dummy', ]
application.names = unique(scrubbed$application)
counts            = unique(scrubbed$interference_counts)  

pdf("app_times.pdf", width=11.5, height=8)
for (app in application.names) {
	data = train_data[train_data$application == app, ]
    
    zero = data[data$interference_count ==0, ]
    one = data[data$interference_count == 1, ]
    two = data[data$interference_count == 2, ]
    three = data[data$interference_count == 3, ]

	minimum = min(data$time)
	maximum = max(data$time)
	lim = c(minimum, maximum)

	caption = paste("Runtimes: ", app)

    stripchart(zero$time, method="jitter", main=caption, col="green", xlim=lim)
    stripchart(one$time, method="jitter", main=caption, col="yellow", xlim=lim, add=TRUE)
    stripchart(two$time, method="jitter", main=caption, col="orange", xlim=lim, add=TRUE)
    stripchart(three$time, method="jitter", main=caption, col="red", xlim=lim, add=TRUE)

	legend("topleft", legend=c("Zero interfering", "One interfering", "Two interfering", "Three interfering"), text.col=c("green", "yellow", "orange", "red"))
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
  median(abs(predict(model, data) - data$time) / data$time) * 100
}

boot.pred_mean = function(data, indices) {
    data = data[indices,]
    median(abs(data)) * 100
}

print('Loading models...')
load(args[3])
print('Loaded models')

print("Models: ")
print(models)

# Plot results

# Create scatter plot of group variance v.s. prediction error
# Group by interference level, colocation level, and nice level

count.used = c()
application.used = c()
model.used = c()
upp.used = c()
low.used = c()
err.used = c()

count.rmse = c()
application.rmse = c()
model.rmse = c()
pred.rmse = c()
base.rmse = c()

# Filter out any column except for our predictors and the response variable
drops = c('application', 'interference_count', 'rep', 'interference')
for (count in counts) {
  count.data = test_data[test_data$interference_count == count, ]
  for (app in application.names) {
    application.data = count.data[count.data$application == app, ]
    
    for (model in names(models[[app]])) {
      fit = models[[app]][[model]]
      fit.boot = boot(data=test.data,
                      statistic=boot.pred,
                      R=999,
                      model=fit,
                      parallel=c('multicore'),
                      ncpus=4)
      ci = boot.ci(fit.boot, type='bca')

      application.used = c(application.used, app)
      count.used = c(count.used, count)
      model.used = c(model.used, model)
      err.used = c(err.used, ci$t0)
      low.used = c(low.used, ci$bca[4])
      upp.used = c(upp.used, ci$bca[5])
    }

    for (interference in unique(application.data$interference) {
      interference.data = application.data[application.data$interference == interference, ]
      data = application.data[ ,!(names(application.data) %in% drops)]
    
      times = data$time

      # Grab the mean as the baseline
      times.mean = mean(times)
      times.abs = times - times.mean
      times.rel = times.abs / times
      times.sd = sd(times.rel)

      # Compute the error for each model, 
      for (model in model.names) {
        mod = models[[app]][[model]]
        print(paste("Model: ", model, ", app: ", app))
        mod_pred = predict(mod, data)
        err.diff = (data$time - pred)
        err.abs = abs(err.diff)
        err.rel = err.abs / data$time
        print(err.abs)
        print(err.rel)
        err.sd = sd(err.rel)
        
        application.rmse = c(application.rmse, app)
        models.rmse = c(model.rmse, model)
        base.rmse = c(base.rmse, times.sd)
        pred.rmse = c(pred.rmse, err.sd)
        count.rmse = c(count.rmse, count)
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


rmse.points = data.frame(application=applications.rmse, count=count.rmse, model=models.rmse, base_rmse=base.rmse, pred_rmse=pred.rmse)

# Plot the base RMSE vs. the prediction RMSE
pdf('base_pred_rmse.pdf', width=11, height=8.5)

# Group by model first
xyplot(pred_rmse ~ base_rmse | count,
       group=model,
       data=err.points,
       auto.key=TRUE,
       xlab="Mean RMSE",
       ylab="Prediction RMSE",
       main="Prediction RMSE v.s. Runtime RMSE",
       par.settings=plot.settings
    )

# Group by application
xyplot(pred_rmse ~ base_rmse | count,
       group=application,
       data=err.points,
       auto.key=TRUE,
       xlab="Mean RMSE",
       ylab="Prediction RMSE",
       main="Prediciton RMSE vs. Runtime RMSE",
       par.settings=plot.settings
    )
dev.off()

error = data.frame(application=application.used, count=count.used, model=model.used, err=err.used, low=low.used, upp=upp.used)

# Sort the rows of error based first on application then group by model
error <- error[order(error$application, error$model),]
#range = extendrange(c(error$error, error$upp, error$low))[2]

pdf("prediction_multi_application.pdf", width=11, height=8.5)
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
