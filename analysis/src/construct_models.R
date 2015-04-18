#!/usr/bin/Rscript


library(Hmisc)
library(rpart)
library(boot)
library(e1071)
library(gbm)
library(elasticnet)
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

# Get configuration informationi
# We don't want dummy inteference data here, since that is only fir baselin
scrubbed = train_data[train_data$interference != 'dummy', ]
application.names   = unique(scrubbed$application)
interference.names  = unique(scrubbed$interference)
reps.indices        = unique(scrubbed$rep)
coloc.levels        = unique(scrubbed$coloc)
nice.levels         = unique(scrubbed$nice)


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

model.names = c("lm", "ridge", "svmRadial", "svmPoly", "gbm")
#model.names = c('lm', 'svmRadial')
#model.names = c('lm')

# Define our formula for y in terms of others
formula=as.formula('time~.')

models = list()

total = length(unique(train_data$rep)) * length(application.names) * length(model.names)
done = 0
print(paste("Total: ", total))

# Build models and use test set for error analysis
#application.names = c('spec_434.zeusmp', 'spec_453.povray') # 'spec_434.zeusmp', 'spec_434.zeusmp')
for (count in unique(train_data$rep)) {
  training.reduced = train_data[train_data$rep <= count, ]
  models[[count]] = list()
  for (app in application.names) {
    
    # Select all rows for our application
    training.set = training.reduced[training.reduced$application == app, ]
    training.set = training.set[training.set$interference != 'dummy', ]

    # Truncate columns that we do not want to be used in the fitting
    drops = c('application', 'interference', 'coloc', 'nice', 'rep')
    training.data = training.set[, !(names(training.set) %in% drops)]

    control.object=trainControl(method='repeatedcv',
                                repeats=10,
                                number=10)

    # Sweep over models
    for (model in model.names) {
      print(paste("Application: ", app, ", model: ", model))
      set.seed(1) 
      # Create a fit mapping from features (no interference) to application performance
      fit = train(form = time ~ .,          
                  data=training.data,
                  method=model,
                  trControl=control.object,
                  preProcess=c("center", "scale"),
                  verbose=FALSE)

      # Save the model for later use
      models[[factor(count)]][[app]][[model]] = fit
      done = done + 1
      print(paste("Finished ", done, " of ", total))
    }
  }
}


print("Saving models...")
save(list=c('models', 'model.names'), file=args[2])
print("Saved models")

warnings()
