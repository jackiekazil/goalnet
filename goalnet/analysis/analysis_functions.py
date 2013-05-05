'''
Created on May 5, 2013

@author: dmasad

A set of functions to analyze model output files.
'''

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
    
    for k, d in data.iteritems():
        tasks = d["tasks"]
        active = 0
        complete = 0
        for t in tasks.values():
            if t['active']: active += 1
            else: complete += 1
        active_tasks.append(active)
        complete_tasks.append(complete)
    return (active_tasks, complete_tasks)
