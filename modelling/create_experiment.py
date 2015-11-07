#!/bin/env python

import numpy as np
import pandas as pd

import util
import sys


fraction_options = [0.1, 0.15, 0.2, 0.25, 0.3]
def get_fractions(idx, max_apps):
    fractions = dict()
    for i in range(2, max_apps + 1):
        fractions[i] = fraction_options[int(idx % len(fraction_options))]
        idx /= len(fraction_options)
    return ','.join(['%(key)s:%(value)s' % locals() for key, value in fractions.items()])
        
def create_experiment(max_apps, reps):
    for rank in [5, 10, 15, 20, 25]:
        for rep in range(reps):
            for idx in range(len(fraction_options)**(max_apps-1)):
                fractions = get_fractions(idx, max_apps)
                print('%(fractions)s %(rank)s %(rep)s' % locals())


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: create_experiment.py maxapps reps')
        sys.exit(1)

    create_experiment(int(sys.argv[1]), int(sys.argv[2]))
