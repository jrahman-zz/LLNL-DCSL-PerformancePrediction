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

import matplotlib.pyplot as plt

import sys
import logging

def main(train_csv, test_csv):
    mods =  {
            'lm': model.LinearModel,
            'ridge': model.RidgeModel,
            'gbm': model.GBMModel,
            'mean': model.MeanModel
            }

    logging.info('Starting model construction...')
    models = cm.construct_models(train_csv.copy(), mods)
    logging.info('Finished base model construction')

    modules = [lc, pe, pm, at, pb]
    for module in modules:
        module = module()
        logging.info('Starting module %s...', str(module))
        module.analyze(train_csv.copy(), test_csv.copy(), models)
        logging.info('Finished module %s', str(module))
    plt.show()

if __name__ == '__main__':
    
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) != 3:
        raise ValueError('Incorrect command line parameters')
    logging.info('Loading data...')
    train_csv = pd.read_csv(sys.argv[1])
    test_csv = pd.read_csv(sys.argv[2])
    logging.info('Loaded data')
    main(train_csv, test_csv)

