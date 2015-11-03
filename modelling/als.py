#!/bin/env python

from pyspark.mllib.recommendation import SparkContext, SparkConf, ALS, MatrixFactorizationModel, Rating
import numpy as np
import sys

def process_line(line):
    return line.strip().split()

def build_ratings(start, next_value):
    ylabels = start[0]
    xlabels = start[1]
    ratings = start[2]
    apps = next_value[0].split('.')
    bubble = next_value[1]
    
    # Fill in matrix with different combinations of the same applications
    for i in range(len(apps)):
        first_app = apps[i]
        remaining_apps = apps[0:i] + apps[i+1:]
        assert(len(remaining_apps) + 1 == len(apps))
        remaining_apps = '.'.join(remaining_apps)
        ratings.append(Rating(int(ylabels[first_app]), int(xlabels[remaining_apps]), float(bubble)))
    return (ylabels, xlabels, ratings)

def build_tuples(start, next_value):
    ylabels = start[0]
    xlabels = start[1]
    tuples = start[2]

    apps = next_value[0].split('.')
    bubble = float(next_value[1])
    
    for i in range(len(apps)):
        first_app = apps[i]
        remaining_apps = '.'.join(apps[0:i] + apps[i+1:])
        tuples.append((int(ylabels[first_app]), int(xlabels[remaining_apps]), bubble))
    return (ylabels, xlabels, tuples)

def main(fraction, rank, rep, data, ylabels, xlabels, ymapping, xmapping):
    train, test = data.randomSplit([fraction, 1 - fraction], rank)
    train = train.aggregate((ylabels, xlabels, []), build_ratings, lambda x, y: x[2] + y[2])
    train = train.flatMap(lambda x: x)
    
    model = ALS.train(ratings, rank, 50)

    test = data.sample(False, 1 - fraction)
    test = test.aggregate((ylabels, xlabels, []), build_tuples, lambda: x, y: x[2] + y[2])
    test = test.flatMap(lambda x: x)

    predictions = model.predictAll(test.map(lambda x: (x[0], x[1]))).map(lambda r: ((r[0], r[1]), r[2]))
    ratings = test.map(lambda x: ((x[0], x[1]), x[2]))
    
    # Both predictions and rating have the form of [(K, V1), ...], [(K, V2), ...] so join both up
    # to the form of [(K, [V1, V2]), ...]
    ratingsAndPreds = ratings.join(predictions)
    
    # Convert back to (yapp, xapps, error) tuples
    return ratingsAndPreds.map(lambda x: (ymapping[x[0][0]], xmapping[x[0][1]], x[1][0] - x[1][1]))

if __name__ == '__main__':
    conf = (SparkConf()
                .setMaster('local')
                .setAppName('PerformancePredictionALS')
                .set('spark.executor.memory', '2g')
    sc = SparkContext(conf = conf)
    f = sc.textFile(sys.argv[1])
    data = f.flatMap(process_file).cache()

    reps = 10
    
    ylabels = {line.split()[0]: int(line.split()[1]) for line in open('ylabels')}
    xlabels = {line.split()[0]: int(line.split()[1]) for line in open('xlabels')}
    ymapping = [line.split()[0] for line in open('ylabels')]
    xmapping = [line.split()[0] for line in open('xlabels')]

    bubble_sizes = {line.strip().split()[0]: float(line.strip().split[1]) for line in open(sys.argv[1])}

    print('apps error bubble rank fraction rep')
    for rank in [5, 10, 15, 20]:
        for fraction in [0.01, 0.1, 0.2, 0.3]:
            for rep in range(reps):
                ratings = main(rank, fraction, rep, data, ylabels, xlabels, ymapping, xmapping)
                for yapp, xapps, error in ratings:
                    apps = '.'.join(sorted([yapp, xapps.split('.')]))
                    bubble = bubble_sizes[apps]
                    print('%(apps)s %(error)f %(bubble)f %(rank)d %(fraction)f %(rep)f' % locals())
