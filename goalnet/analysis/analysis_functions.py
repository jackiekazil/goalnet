'''
Created on May 5, 2013

@author: dmasad

A set of functions to analyze model output files.
'''
import json
import exceptions

OUTPUT_PATH = "../outputs/"

'''
HELPER FUNCTIONS
================
'''

def to_num(s):
    '''
    Try to convert a string to a number
    '''
    try:
        return int(s)
    except exceptions.ValueError:
        try:
            return float(s)
        except:
            return s

def recode_dict(data_raw):
    '''
    Recursively convert dictionary string keys to numbers.
    '''
    data_clean = {}
    for key, val in data_raw.iteritems():
        key_clean = to_num(key)
        if type(val) is dict:
            val_clean = recode_dict(val)
        elif type(val) is str:
            val_clean = to_num(val)
        else: val_clean = val
        data_clean[key_clean] = val_clean
    return data_clean

def load_data(path):
    '''
    Load a data file, and convert number-strings to numbers.
    '''
    with open(path) as f:
        data_raw = json.load(f)
    data = recode_dict(data_raw)
    return data

'''
ANALYSIS FUNCTIONS
==================
'''

def count_tasks(data):
    '''
    Count the active and completed tasks at each time-step.
    '''
    active_tasks = []
    complete_tasks = []
    keys = sorted(data.keys())
    for key in keys:
        tasks = data[key]["tasks"]
        active = 0
        complete = 0
        for t in tasks.values():
            if t['active']: active += 1
            else: complete += 1
        active_tasks.append(active)
        complete_tasks.append(complete)
    return (keys, active_tasks, complete_tasks)

def get_ginis(data):
    '''
    Get the gini coefficient for each timestep.
    '''
    keys = sorted(data.keys())
    ginis = []
    
    for key in keys:
        wealths = sorted(data[key]["wealth"].values())
        sum_iy = 0
        sum_y = 0
        n = len(wealths)
        for i, y in enumerate(wealths):
            sum_iy += i*y
            sum_y += y
        if sum_y > 0:
            gini = ((2.0*sum_iy)/(n*sum_y)) - ((n + 1.0)/n)
        else:
            gini = 0
        ginis.append(gini)
    return ginis
        