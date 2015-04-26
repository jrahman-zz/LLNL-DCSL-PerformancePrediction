import model
import pandas as pd

import construct_models as cm

import pca_analysis as pca
import application_times as at
import prediction_error as pe
import prediction_rmse as pm
import prediction_bias as pb

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

    models = cm.construct_models(train_csv.copy(), mods)
    plots = []
    modules = [pe, pm, at, pb]
    for module in modules:
        module.analyze(train_csv.copy(), test_csv.copy(), models)
    plt.show()

if __name__ == '__main__':
    
    logging.basicConfig(level=logging.DEBUG)
    
    if len(sys.argv) != 3:
        raise ValueError('Incorrect command line parameters')
    train_csv = pd.read_csv(sys.argv[1])
    test_csv = pd.read_csv(sys.argv[2])
    main(train_csv, test_csv)

