#!/usr/bin/env python
import model
import pandas as pd

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

def main(train_csv, test_csv, pool_size, suffix, prefix):
    mods =  {
            'lm': model.LinearModel,
            'ridge': model.RidgeModel,
            'gbm': model.GBMModel,
            'mean': model.MeanModel
            }

    logging.info('Starting model construction...')
    models = cm.construct_models(train_csv.copy(), mods)
    logging.info('Finished base model construction')

    modules = [pe, pm, pb, tss, lc, fs, pca]
    pool = Pool(pool_size)

    # Instantiate each module for use
    modules = [module() for module in modules]
    results = [pool.apply_async(run, (module, train_csv.copy(), test_csv.copy(), models, prefix, suffix)) for module in modules]
    finished = [result.get() for result in results]

if __name__ == '__main__':
    
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) != 3:
        raise ValueError('Incorrect command line parameters')
    logging.info('Loading data...')
    train_csv = pd.read_csv(sys.argv[1])
    test_csv = pd.read_csv(sys.argv[2])
    logging.info('Loaded data')
    main(train_csv, test_csv, 4, 'spec', 'pdf')

