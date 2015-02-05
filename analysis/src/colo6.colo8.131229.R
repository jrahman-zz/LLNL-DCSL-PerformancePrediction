# Predict measurement benchmarks from single interference to double/triple interference.

error.bar <- function(x, y, upper, lower=upper, length=0.1,...){
  if(length(x) != length(y) | length(y) !=length(lower) | length(lower) != length(upper))
    stop("vectors must be same length")
  arrows(x,y+upper, x, y-lower, angle=90, code=3, length=length, ...)
}

error.bar.horiz <- function(x, y, upper, lower=upper, length=0.1,...){
  if(length(x) != length(y) | length(y) !=length(lower) | length(lower) != length(upper))
    stop("vectors must be same length")
  arrows(y+upper, x, y-lower, x, angle=90, code=3, length=length, ...)
}

library(boot)

boot.stat=function(data, indices) {
  median(data[indices])*100
}

library(caret)
# factors are evil
d=read.csv('colo6.colo7.131229.csv.gz', head=F, sep=' ', stringsAsFactors=F)
names(d)=c('measure','x1','x2','y','i')
single.env=read.csv("colo6.train.131229.csv.gz", head=T, sep=" ", stringsAsFactors=F)
triple.env=read.csv("colo7.test.131229.csv.gz", head=T, sep=" ", stringsAsFactors=F)

xNames=c("fs_create_1000", "fs_delete_1000", "memory_random_1e3",
         "memory_random_1e6", "memory_random_1e9", "memory_stream_1e3",
         "memory_stream_1e6", "memory_stream_1e9", "read1G", "read4M", "read64M",
         "stream_Add", "stream_Copy", "stream_Scale", "stream_Triad", "write1G",
         "write4M", "write64M")
yNames=c("cassandra.sh_10000", "mongodb.sh_10000", "voldemort.sh_10000",
         "spec.GemsFDTD", "spec.astar", "spec.bwaves", "spec.bzip2", "spec.cactusADM",
         "spec.calculix", "spec.dealII", "spec.gamess", "spec.gcc", "spec.gobmk",
         "spec.gromacs", "spec.h264ref", "spec.hmmer", "spec.lbm", "spec.leslie3d",
         "spec.libquantum", "spec.mcf", "spec.milc", "spec.namd", "spec.omnetpp",
         "spec.perlbench", "spec.povray", "spec.sjeng", "spec.soplex", "spec.sphinx3",
         "spec.tonto", "spec.wrf", "spec.xalancbmk", "spec.zeusmp")

modelNames=c('lm')
formula.env=as.formula('y~x1+x2')
pr=list()
er=list()
ci=list()
ci.app=list()
pred.app=list()
fit.app=list()

pdf("predict_environment_double_bootstrap.pdf", width=10, height=8)

controlObject=trainControl(method='repeatedcv', repeats=5, number=10)
allEnv=unique(d$i)
set.seed(1)
# trainRows=createDataPartition(1:length(allEnv), p=.8, list=F)
trainFolds=createFolds(1:length(allEnv), returnTrain=T)

for (model in modelNames) {
  pr[[model]]=matrix(0, length(allEnv), length(xNames))
  rownames(pr[[model]])=allEnv
  colnames(pr[[model]])=xNames
  
  er[[model]]=matrix(0, length(allEnv), length(xNames))
  rownames(er[[model]])=allEnv
  colnames(er[[model]])=xNames
  
  for (y in yNames) {
    trainSet.app=single.env[single.env[,y]>0,]
    if (nrow(trainSet.app)==0) {
      next
    }
    formula.app=as.formula(paste(y,"~",paste(xNames,collapse="+"),sep=""))
    set.seed(1)
    fit.app[[model]][[y]]=train(formula.app, data=trainSet.app, method=model,
                                trControl=controlObject)
  }
  
  for (trainRows in trainFolds) {
    trainEnv=allEnv[trainRows]
    testEnv=allEnv[-trainRows]
  
    # STEP 1: Predict complex env from simple env
    for (measurement in xNames) {
      measurementData=d[d[,1]==measurement,]
      rownames(measurementData)=measurementData[,ncol(measurementData)]
      trainSet=measurementData[trainEnv,]
      testSet=measurementData[testEnv,]
      
      set.seed(1)
      fit=train(formula.env, data=trainSet, method=model, trControl=controlObject)
      pr[[model]][testEnv, measurement]=predict(fit, testSet)
      er[[model]][testEnv, measurement]=abs(predict(fit, testSet)-testSet$y)/testSet$y
    }
    
    # STEP 2: Predict app from env
    for (y in yNames) {
      if (!y %in% colnames(triple.env)) {
        next
      }
      tripleTestSet=triple.env[triple.env$INTERF %in% testEnv & triple.env[,y]>0,]
      if (nrow(tripleTestSet)==0) {
        next
      }
      for (e in unique(tripleTestSet$INTERF)) {
        origY=tripleTestSet[tripleTestSet$INTERF==e, y]
        predY=predict(fit.app[[model]][[y]], as.data.frame(t(pr[[model]][match(e, allEnv),])))
        pred.app[[model]][[y]]=c(pred.app[[model]][[y]], abs(predY-origY)/origY)
      }
    }
  }
  
  for (measurement in xNames) {
    bt=boot(data=er[[model]][,measurement], statistic=boot.stat, R=999)
    # see for bca: "Better Bootstrap Confidence Intervals" by Efron 1987.
    # see "Bootstrapping Regression Models" by John Fox 2002.
    ci[[model]][[measurement]]=boot.ci(bt, type="bca")
  }
  
  par(mar=c(4,10,1,0), xpd=T)
  err=sapply(ci[[model]], function(x) x$t0)
  low=sapply(ci[[model]], function(x) x$bca[4])
  upp=sapply(ci[[model]], function(x) x$bca[5])
  bars = barplot(err,
                 beside=T, las=1, horiz=T,
                 xlim=c(0, extendrange(c(err, upp, low))[2]),
                 xlab='Median Prediction Error %',
                 col="green", border='white')
  error.bar.horiz(bars, err, upp-err, err-low, col='gray')
  text(round(err, 1), bars, round(err, 1), adj=c(0,0.5))
  
  for (y in yNames) {
    if (y %in% names(pred.app[[model]])) {
      bt.app=boot(data=pred.app[[model]][[y]], statistic=boot.stat, R=10000)
      ci.app[[model]][[y]]=boot.ci(bt.app, type="bca")
    }
  }
  par(mar=c(4,10,1,0), xpd=T)
  err.app=sapply(ci.app[[model]], function(x) x$t0)
  low.app=sapply(ci.app[[model]], function(x) x$bca[4])
  upp.app=sapply(ci.app[[model]], function(x) x$bca[5])
  bars.app = barplot(err.app,
                 beside=T, las=1, horiz=T,
                 xlim=c(0, extendrange(c(err.app, upp.app, low.app))[2]),
                 xlab='Median Prediction Error %',
                 col="green", border='white')
  error.bar.horiz(bars.app, err.app, upp.app-err.app, err.app-low.app, col='gray')
  text(round(err.app, 1), bars.app, round(err.app, 1), adj=c(0,0.5))
}

dev.off()