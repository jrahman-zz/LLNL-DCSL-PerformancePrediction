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
library(caret)

# Perform single application prediction
#
# Take a set of feature benchmarks along with application runtimes
# and create a model of the application runtime as a function of the
# feature benchmarks
#

# Benchmark names
# TODO, update this later with our actual feature names
feature.names=c("fs_create_1000", "fs_delete_1000", "memory_random_1e3",
         "memory_random_1e6", "memory_random_1e9", "memory_stream_1e3",
         "memory_stream_1e6", "memory_stream_1e9", "read1G", "read4M", "read64M",
         "stream_Add", "stream_Copy", "stream_Scale", "stream_Triad", "write1G",
         "write4M", "write64M")

# Application names
# TODO, update with actual and new application names
#application.names=c("cassandra.sh_10000", "mongodb.sh_10000", "voldemort.sh_10000",
#         "spec.GemsFDTD", "spec.astar", "spec.bwaves", "spec.bzip2", "spec.cactusADM",
#         "spec.calculix", "spec.dealII", "spec.gamess", "spec.gcc", "spec.gobmk",
#         "spec.gromacs", "spec.h264ref", "spec.hmmer", "spec.lbm", "spec.leslie3d",
#         "spec.libquantum", "spec.mcf", "spec.milc", "spec.namd", "spec.omnetpp",
#         "spec.perlbench", "spec.povray", "spec.sjeng", "spec.soplex", "spec.sphinx3",
#         "spec.tonto", "spec.wrf", "spec.xalancbmk", "spec.zeusmp")

# Read in data
d=read.csv('../test/single_app.csv',
           head=T,
           sep=',',
           stringsAsFactors=T)

# Set data frame names appropriately
#metadata = c("application", "interference") # This won't be needed with the new data format
#names(d) = c(metadata, features.names)

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

model.names = c("lm", "svmLinear")

# Define our formula for y in terms of others
formula=as.formula('y~.')

ci=list()

# Sweep over applications
for (application in unique(d$application)) {
  
  # Select all rows for our application
  data = d[d$application == application, ]
  
  # Partition the data into training and validation sets
  training.rows=createDataPartition(data$y, p=.7, list=F)
  training.set=data[training.rows, ]
  test.set=data[-training.rows, ]
  
  print(training.set)
  print(test.set)
  
  drops = c('application', 'interference')
  training.data = training.set[, !(names(training.set) %in% drops)]
  testing.data = test.set[, !(names(test.set) %in% drops)]
  
  # Sweep over models
  for (model in model.names) {
    
    control.object=trainControl(method='repeatedcv', repeats=5, number=10)
    set.seed(1)
    
    # Create a fit mapping from features (no interference) to application performance
    fit=train(form = y ~ ., data=training.data, method=model, trControl=control.object)
    
    fit.boot=boot(data=testing.data, statistic=boot.pred, R=999, model=fit)
    # see for bca: "Better Bootstrap Confidence Intervals" by Efron 1987.
    # see "Bootstrapping Regression Models" by John Fox 2002.  
    ci[[application]][[model]]=boot.ci(fit.boot, type="bca")
  }
}

# Plot results
pdf("predict_application_clean_environment.pdf", width=10, height=5)
par(mar=c(10,4,1,0), xpd=T)
err=sapply(ci, function(x) x$lm$t0)
low=sapply(ci, function(x) x$lm$bca[4])
upp=sapply(ci, function(x) x$lm$bca[5])
bars = barplot(err,
               beside=T, las=3, cex.names=0.8,
               ylim=c(0, extendrange(c(err, upp, low))[2]),
               ylab='Median Prediction Error %',
               col="green", border='white')
error.bar(bars, err, upp-err, err-low)
text(bars, 0, round(e, 1), srt=90, adj=c(0,0.5), cex=0.8)
dev.off()
