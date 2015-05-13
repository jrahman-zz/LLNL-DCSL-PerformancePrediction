import sqlite3
import logging
import math

import pandas as pd
import numpy as np

import scikits.bootstrap as boot

import matplotlib
import matplotlib.pyplot as plt


def rmse_error(y, pred):
    err = math.sqrt(sum((y - pred)**2) / len(y)) / np.mean(y) * 100
    return err

def relative_error(y, pred):
    err = (y - pred) / y * 100
    return err

def drops():
    """ Store list of non-predictor/non-response columns """
    drops = [
            'application',
            'interference',
            'coloc',
            'cores',
            'nice',
            'rep'
            ]
    return drops

def get_predictors(data):
    """ Get all predictor columns from a DataFrame """
    dropped = drops()
    dropped.append('time')
    d = set()
    for drop in dropped:
        d.add(drop)
    columns = []
    for column in data.columns:
        if column not in d:
            columns.append(column)
    return data[columns]

def get_nonmetadata(data):
    """ Get all non-metadata columns from a DataFrame """
    dropped = drops()
    d = set()
    for drop in dropped:
        d.add(drop)
    columns = []
    for column in data.columns:
        if column not in d:
            columns.append(column)

    return data[columns]

def get_nontime(data):
    """ Retrieve all non-time columns from a DataFrame """
    columns = []
    for column in data.columns:
        if column != 'time':
            columns.append(columns)
    return data[columns]

def drop_metadata(data):
    for drop in drops():
        if drop in data:
            del data[drop]
    return data


def bootstrap(data, statistic, samples=1000):
    return boot.ci(data, statfunction=statistic, n_samples=samples)

def median(data):
    return np.median(data)

def plot_prep(backend='PS'):
    matplotlib.style.use('ggplot')

def load_csv(f, header=True, sep=','):
    first_line = True
    
    row = 1
    headers = []
    data = []

    for line in f.xreadlines():
        elements = line.split(sep)
        elements[-1] = elements[-1].rstrip('\n')
        if first_line:
            print line
            first_line = False
            if header:
                headers = elements
                continue
            headers = range(1, len(elements) + 1)
        data.append(elements)
    headers = [str(x) for x in headers]

    return (headers, data)

def load_data(filename):
    return pd.read_csv(filename)


def frange(start, stop, step=1):
    """ Provide range() functionality but with non-integer step sizes """
    if start >= stop:
        raise ValueError('start >= stop')
    if step <= 0:
        raise ValueError('step <= 0')

    step_count = int(math.floor((stop - start) / step))
    return [start + i * step for i in range(0, step_count)]

def load_db(filename, dbname):

#    conn = sqlite3.connect(':memory:')
    conn = sqlite3.connect(dbname)
    conn.isolation_level = 'DEFERRED'
    c = conn.cursor()

    with open(filename, 'r') as f:
        (header, values) = load_csv(f)

        indexes = []
        columns = []
        column_names = []
        for i in range(0, len(header)):
            val = values[0][i]
            if isinstance(val, str):
                data_type = 'text'
                indexes.append(header[i])
            elif isinstance(val, float):
                data_type = 'real'
            elif isinstance(val, int):
                data_type = 'integer'
                indexes.append(header[i])
            column_name = '%s %s' % (header[i], data_type)
            columns.append(column_name)
            column_names.append(header[i])
        query = '''CREATE TABLE data (%s)''' % (', '.join(columns))
        logging.info('Executing query: %s', query)
        c.execute(query)

        marks = ['?' for i in range(0, len(header))]
        query = 'INSERT INTO data VALUES (%s)' % (','.join(marks))
        c.executemany(query, values)

        # Build our index on textual columns
        query = '''CREATE INDEX index%d ON data (%s)'''
        for i in range(0, len(indexes)):
            c.execute(query % (i, indexes[i]))

        query = '''CREATE TABLE colnames (name text)'''
        c.execute(query)

        query = 'INSERT INTO colnames VALUES (?)'
        insert = [(x,) for x in column_names]
        c.executemany(query, insert)
        conn.commit()
    return conn

def _build_select(conn, columns, where, orderby):
    if len(columns) == 0:
        query = '''SELECT name FROM colnames'''
        columns = [x[0] for x in conn.execute(query)]

    if orderby != '':
        orderby = " AND (%s)" % (orderby)
    if where != '':
        where = "WHERE %s" % (where)

    query = '''%s FROM data %s ORDER BY rowid %s''' %  (', '.join(columns), where, orderby)
    return (query, columns)

def _process_select(conn, query, columns):
    logging.info('Query: %s', query)
    data = []
    for row in conn.execute(query):
        data.append([x for x in row])
    cols = dict()
    for i in range(0, len(columns)):
        cols[columns[i]] = i
    return (cols, data)

def select(conn, columns=[], where='', orderby=''):
    (query, columns) = _build_select(conn, columns, where, orderby)
    query = '''SELECT %s''' % (query)
    return _process_select(conn, query, columns)

def select_distinct(conn, columns=[], where='', orderby=''):
    (query, columns) = _build_select(conn, columns, where, orderby)
    query = '''SELECT DISTINCT %s''' % (query)
    return _process_select(conn, query)
