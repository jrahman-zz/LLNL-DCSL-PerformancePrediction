#!/usr/bin/Rscript
library(Hmisc)
library(rpart)
library(e1071)
library(gbm)
library(MASS)
library(lars)
library(pls)
library(glmnet)
library(genalg)
library(caret)

# Benchmark names
xNames=c("fs_create_1000", "fs_delete_1000", "memory_random_1e3",
         "memory_random_1e6", "memory_random_1e9", "memory_stream_1e3",
         "memory_stream_1e6", "memory_stream_1e9", "read1G", "read4M", "read64M",
         "stream_Add", "stream_Copy", "stream_Scale", "stream_Triad", "write1G",
         "write4M", "write64M")

# Application names
yNames=c("cassandra.sh_10000", "mongodb.sh_10000", "voldemort.sh_10000",
         "spec.GemsFDTD", "spec.astar", "spec.bwaves", "spec.bzip2", "spec.cactusADM",
         "spec.calculix", "spec.dealII", "spec.gamess", "spec.gcc", "spec.gobmk",
         "spec.gromacs", "spec.h264ref", "spec.hmmer", "spec.lbm", "spec.leslie3d",
         "spec.libquantum", "spec.mcf", "spec.milc", "spec.namd", "spec.omnetpp",
         "spec.perlbench", "spec.povray", "spec.sjeng", "spec.soplex", "spec.sphinx3",
         "spec.tonto", "spec.wrf", "spec.xalancbmk", "spec.zeusmp")

# Training set
train=read.csv("../data/colo6.test.131229.csv.gz", head=T, sep=" ")

# Testing set
test=read.csv("../data/colo7.test.131229.csv.gz", head=T, sep=" ")

match.rows = function(test.col, train.data) {
  grep(unlist(strsplit(test.col, ":"))[1], train.data$INTERF)
}

compute.error = function(y0, y1) {
  abs(y1[[1]][[1]] - y0)/y0
}

# do.predict = function(y, xNames, train.set, test.set) {
#   train.set2 = train.set[train.set[,y]>0,]
#   if (nrow(train.set2) == 0)
#     return
#   test.set2 = test.set[test.set[,y]>0,]
#   if (nrow(test.set2) == 0)
#     return
#   xNames2 = xNames[colSums(train.set2[,xNames])>0]
#   
#   #LM
#   model.formula = as.formula(paste(y,"~",paste(xNames2,collapse="+"),sep=""))
#   fit = lm(model.formula, data = train.set2)
#   compute.error(test.set2[,y], predict(fit, test.set2))
# }
# 
# predict.wrapper = function(test.set, train.set, yNames, xNames) {
#   error = list()
#   for (y in yNames) {
#     e = do.predict(y, xNames, train.set, test.set)
#     if (length(e) > 0) {
#       error[[y]] = e
#     }
#   }
#   error
# }
# 
# result = ddply(test, .(INTERF), predict.wrapper, train, yNames[1], xNames)

model.formula = list()
model.fit = list()
model.error = list()

# Sweep over all the applications
for (y in yNames) {
  # Sweep over all the levels
  for (i in levels(test$INTERF)) {

    test.set = test[test$INTERF == i,]
    test.set = test.set[test.set[,y]>0,]
    if (nrow(test.set) == 0)
      next
   
    # Preprocess training set    
    train.rows = lapply(unlist(strsplit(as.character(test.set$INTERF[1]), ",")), 
                        match.rows, train)
    train.set = train[unlist(train.rows),]
    train.set = train.set[train.set[,y]>0,]
    print(train.set)

    if (nrow(train.set) == 0)
      next
    
    xNames2 = xNames[colSums(train.set[,xNames])>0]

    model.formula[[y]][[i]] = as.formula(paste(y,"~",paste(xNames2,collapse="+"),sep=""))
    
    # Compute the linear model for pairing of interference i and app y
    model.fit[[y]][[i]] = lm(model.formula[[y]][[i]], data = train.set)
    model.error[[y]][[i]] = compute.error(test.set[,y], predict(model.fit, test.set))
  }
}

# Plotting results
pdf("colo7.131229.pdf", width=10, height=5)
par(mar=c(10,4,1,0), xpd=T)
d = sapply(model.error, function(x) median(unlist(x)))*100
b = barplot(d,
            beside=T, las=3, cex.names=0.8,
            ylab='Median Prediction Error %',
            col="green", border='white',
            ylim=c(0,100))
text(b, 0, floor(d), srt=90, adj=c(0,0.5), cex=0.8)

d = sapply(model.error, length)
b = barplot(d,
            beside=T, las=3, cex.names=0.8,
            ylab='Number of Samples',
            col="yellow", border='white')
text(b, 0, floor(d), srt=90, adj=c(0,0.5), cex=0.8)
dev.off()
