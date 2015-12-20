#!/bin/env python

import pyspark
from pyspark import SparkContext, SparkConf
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
import numpy as np

import random
import itertools
import sys
import json
import requests
import logging

data_file = 'als_data'

def parse_experiement(exp):
    """
    Format: 'appcount:fraction,appcount:fraction,...,appcount:fraction rank rep'
    Note that we define a different fraction per application count
    so we can vary the density for each section of the matrix
    """

    parsed_experiement = dict()
    parsed_experiement['fractions'] = {int(pair.split(':')[0]): float(pair.split(':')[1]) for pair in exp.split()[0].split(',')}
    parsed_experiment['rank'] = int(exp.split()[1])
    parsed_experiment['rep'] = int(exp.split()[2])
    return parsed_experiement

def create_training_data(bubble_sizes, fractions, app_count, max_column_apps):
    """
    Create training data for ALS algorithm based on sparse sub-set of total data
    bubble_sizes: Dictionary of app1.app2...appN => bubble_size mappings
    fraction: Dictionary of appCount => fraction mappings
    max_row_apps: Maximum number of apps in the row key
    max_column_apps: Maximum number of apps in the column key
    """

    # Track the valid column keys and number of entries that could fit in that column
    column_keys = dict()
    for column_count in range(1, max_column_apps + 1):
        for app_set in bubble_sizes:
            if len(app_set.split('.')) == (1 + column_count)
                for key in itertools.combination(app_set.split('.'), column_count):
                    key = '.'.join(sorted(key))
                    if key not in column_keys:
                        column_keys[key] = 0
                    column_keys[key] += 1

    # Collect the number of entries for each group based on batch application count
    total_entries = {app_count: sum([len(apps.split('.')) for apps in bubble_sizes if len(apps.split('.')) == app_count]) for app_count in range(1, max_column_apps + 2)
    
    # Initialize with a zero filled entry count
    filled_entries = {app_count: 0 for app_count in range(1, max_column_apps + 1)}

    # Store row_key:column_key pairs for each entry
    training_data = dict()

    # Now based on the known proportions of data, select a sub-set of the data and fill columns
    # we start with empty columns first, only moving to add additional data later
    for size in range(1, max_column_apps + 1):
        keys = [key for key in column_keys.keys() if len(key.split('.')) == size]
        while float(filled_entries[size + 1]) / float(total_entries[size + 1]) < fractions[size + 1]:
            # Loop over all the app combinations
            for key in bubble_data:
                if len(key)
