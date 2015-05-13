#!/usr/bin/env python
import model
import pandas as pd

import argparse

import construct_models as cm

from pca_analysis import PcaAnalysis as pca
from application_times import ApplicationTimes as at
from prediction_error import PredictionError as pe
from prediction_rmse import PredictionRmse as pm
from prediction_bias import PredictionBias as pb
from learning_curves import LearningCurves as lc
from train_set_size import TrainingSetSize as tss
from feature_selection import FeatureSelection as fs

from multiprocessing import Pool

import sys
import logging

def run(module, train, test, models, prefix, suffix):
    try:
        logging.info('Starting module %s....', str(module))
        module.analyze(train, test, models)
        logging.info('Finished running module %s', str(module))
        logging.info('Plotting module %s...', str(module))
        module.plot(prefix, suffix)
        logging.info('Finished plotting module %s', str(module))
        return module
    except Exception as e:
        logging.exception('Error: %s', str(e))
        return None

def main(train_csv, test_csv, pool_size, prefix, suffix):
    mods =  {
            'lm': model.LinearModel,
            'ridge': model.RidgeModel,
            'gbm': model.GBMModel,
            'svmlinear': model.SVMLinearModel,
            'mean': model.MeanModel
            }

    logging.info('Starting model construction...')
    models = cm.construct_models(train_csv.copy(), mods)
    logging.info('Finished base model construction')

    modules = [pe, pm, pb, tss, lc, pca]
    pool = Pool(pool_size)

    # Instantiate each module for use
    modules = [module() for module in modules]
    results = [pool.apply_async(run, (module, train_csv.copy(), test_csv.copy(), models, prefix, suffix)) for module in modules]
    finished = [result.get() for result in results]

if __name__ == '__main__':
    
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description='Run analysis for models')
    parser.add_argument('train_data', type=str)
    parser.add_argument('test_data', type=str)
    parser.add_argument('pool_size', type=int, default=4)
    parser.add_argument('prefix', type=str)
    parser.add_argument('suffix', type=str)
    args = parser.parse_args()

    logging.info('Loading data...')
    train_csv = pd.read_csv(args.train_data)
    test_csv = pd.read_csv(args.test_data)
    logging.info('Loaded data')
    main(train_csv, test_csv, args.pool_size, args.prefix, args.suffix)

