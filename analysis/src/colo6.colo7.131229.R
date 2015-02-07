# Predict measurement benchmarks from single interference to double interference.

error.bar <- function(x, y, upper, lower=upper, length=0.1,...){
  if(length(x) != length(y) | length(y) !=length(lower) | length(lower) != length(upper))
    stop("vectors must be same length")
  arrows(x,y+upper, x, y-lower, angle=90, code=3, length=length, ...)
}

library(boot)

boot.pred=function(data, indices, model) {
  data=data[indices,]
  median(abs(predict(model, data)-data$y)/data$y)*100
}

library(caret)

# Pull in data from compressed csv file
d=read.csv('../data/colo6.colo7.131229.csv.gz', sep=' ', head=F)

# Set data frame names appropriately
names(d)=c('measure','x1','x2','y')

# Ok, these are the benchmark types
xNames=c("fs_create_1000", "fs_delete_1000", "memory_random_1e3",
         "memory_random_1e6", "memory_random_1e9", "memory_stream_1e3",
         "memory_stream_1e6", "memory_stream_1e9", "read1G", "read4M", "read64M",
         "stream_Add", "stream_Copy", "stream_Scale", "stream_Triad", "write1G",
         "write4M", "write64M")

# Use different models
modelNames=c('lm')


formula=as.formula('y~.')
ci=list()
for (measurement in xNames) {
  for (model in modelNames) {
    # TODO, what does this line do
    data=d[d[,1]==measurement,2:ncol(d)]
    set.seed(1)
    
    # Partition the data into training and validation sets
    trainingRows=createDataPartition(data$y, p=.8, list=F)
    trainingSet=data[trainingRows,]
    testSet=data[-trainingRows,]

    # TODO, research trainControl
    controlObject=trainControl(method='repeatedcv', repeats=5, number=10)
    set.seed(1)

    fit=train(formula, data=trainingSet, method=model, trControl=controlObject)
    
    # TODO, research the bootstrapping method
    fit.boot=boot(data=testSet, statistic=boot.pred, R=999, model=fit)
    # see for bca: "Better Bootstrap Confidence Intervals" by Efron 1987.
    # see "Bootstrapping Regression Models" by John Fox 2002.  
    ci[[measurement]][[model]]=boot.ci(fit.boot, type="bca")
  }
}

# Plot results
pdf("predict_environment_double_bootstrap.pdf", width=10, height=5)
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
