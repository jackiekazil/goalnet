'''
Created on May 5, 2013

@author: dmasad

A set of functions to analyze model output files.
'''
import json
import os
import exceptions
import networkx as nx

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

def iterate_over_data(base_path):
    '''
    Iterate over data files, loading and yielding one at a time.
    '''
    for run_dir in os.listdir(base_path):
        try:
            yield load_data(base_path + run_dir + "/data.json")
        except:
            pass


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


'''
NETWORK ANALYSIS FUNCTIONS
'''

def iterate_over_networks(base_path):
    '''
    Iterate over network files, loading and yielding one at a time.
    '''
    for run_dir in os.listdir(base_path):
        try:
            yield nx.read_graphml(base_path + run_dir + "/last_task_graph.graphml")
        except:
            pass


def get_agent_data(G):
    '''
    Get the agent attributes and stats loaded from a model output graph.

    Returns a list of dictionaries.
    '''
    agent_count = len(G)
    agent_data = []

    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)
    for node, params in G.nodes(data=True):
        node_data = params
        node_data['in_deg'] = G.in_degree(node)
        node_data['out_deg'] = G.out_degree(node)
        node_data['closeness'] = closeness[node]
        node_data['betweenness'] = betweenness[node]
        node_data['total_agent_count'] = agent_count
        agent_data.append(node_data)
    return agent_data


def get_network_statistics(G):
    '''
    Compute key nework statistics for 
    '''
    size = len(G)
    density = nx.density(G)
    #diameter = nx.diameter(G)

    clustering = nx.average_clustering(G.to_undirected())
    transitivity = nx.transitivity(G.to_undirected())
    grc = global_reaching_centrality(G)
    return {"size": size,
            "density": density,
            #"diameter": diameter,
            "clustering": clustering,
            "transitivity": transitivity,
            "grc": grc}





def global_reaching_centrality(G):
    '''
    Compute the Global Reaching Centrality measure of heirarchy.
    
    '''

    reaching_scores = nx.closeness_centrality(G).values()
    cr_max = max(reaching_scores)
    grc = 0
    for cr in reaching_scores:
        grc += (cr_max - cr)
    grc = grc / (len(reaching_scores) - 1.0)
    return grc