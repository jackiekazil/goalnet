'''
GoalNet Data Collector
======================

@author: dmasad
'''

from collections import defaultdict
import json
import csv
import uuid
import os

import networkx as nx

class DataCollector(object):
    '''
    This class collects data from the world.
    
    Overall structure:
        data is a dictionary that will contain all the data collected. Each key
        is a timestamp at which data has been collected.
    
    '''


    def __init__(self, world):
        '''
        Create a new Data Collector and link it to the World object.
        
        Args:
            world: The world object to collect data on.
        '''
        self.world = world
        self.data = defaultdict(dict)
        self.uuid = uuid.uuid4()
    
    '''
    DATA COLLECTION FUNCTIONS
    '''
    
    def collect_wealth(self):
        '''
        Collect the current wealth variable for all agents.
        '''    
        wealths = {}
        for agent_id, agent in self.world.agents.items():
            wealths[agent_id] = agent.wealth
        return wealths
    
    def collect_tasks(self):
        '''
        Collects data on all tasks.
        '''
        task_data = {}
        for task_id, task in self.world.tasks.items():
            task_data[task_id] = task.__dict__
        return task_data
    
    def collect_network(self):
        '''
        Collects the current state of the network.
        '''
        return self.world.network.copy()
    
    def collect_task_network(self, include_data = True):
        '''
        Collects data on the network formed by the task performance relationships.
        
        Returns a directed graph, with edges directed to the task owner.
        
        Args:
            include_data: if True, include node attributes.
        
        '''
        task_network = nx.DiGraph()
        for task_id, task in self.world.tasks.iteritems():
            for worker in task.workers:
                task_network.add_edge(worker, task.owner)
        
        if not include_data:
            return task_network
        
        for agent_id in task_network.nodes():
            agent = self.world.agents[agent_id]
            task_network.node[agent_id]['wealth'] = float(agent.wealth)
            task_network.node[agent_id]['greed'] = float(agent.greed)
            task_network.node[agent_id]['centralization'] = float(agent.centralization)
        return task_network
            
    
    def willingness_to_help(self):
        '''
        Collects the data on each agent's Willingness to Help others
        The dictionary has, {key: agent_id, value: [(agent1, WTH),(agent2, WTH),...]}
        '''
        willingness_to_help = {}
        for agent_id, agent in self.world.agents.items():
            current_wth = {}
            for key, val in agent.wth.items():
                current_wth[key] = val
            willingness_to_help[agent_id] = current_wth
        
        return willingness_to_help
    
    def collect_all_data(self):
        '''
        Run all data collection functions and update the data dictionary.
        '''
        clock = self.world.clock
        current_data = {}
        
        current_data["wealth"] = self.collect_wealth()
        current_data["tasks"] = self.collect_tasks()
        current_data["network"] = self.collect_network()
        current_data["task_network"] = self.collect_task_network()
        current_data["willingness_to_help"] = self.willingness_to_help()
        #TODO: Add more functions here
        
        self.data[clock] = current_data
    
    
    '''
    DATA OUTPUT FUNCTIONS
    '''
        
    def export(self):
        '''
        Export all data.
        '''
        path = "../outputs/" + str(self.uuid)
        os.mkdir(path)
        path += "/"
        
        # Save configuration
        with open(path + "config.json", "wb") as f:
            json.dump(self.world.config, f)
        
        # Write the time series of dicts
        self.write_json(path + "data.json")
        
        # Write last task graph
        last_task_graph = self.data[max(self.data)]["task_network"]
        nx.write_graphml(last_task_graph, path+"last_task_graph.graphml")
        
    
    
    def write_json(self, filepath):
        '''
        Export all the data collected so far to one big json.
        '''
        json_out = {}
        for key in self.data:
            current_out = {}
            for var in ["wealth", "tasks", "willingness_to_help"]:
                current_out[var] = self.data[key][var]
            json_out[key] = current_out

        with open(filepath, "wb") as f:
            json.dump(json_out, f)
    
    def write_dict_csv(self, filepath, key):
        '''
        Write a csv containing a time series of a dictionary.
        
        Each row will be a timestamp, and each column will be a dictionary
        key. 
        For example: if key == "wealth", each column will be an agent, and each
        row will be the agent's wealth at that timestamp.
         
        '''
        # Assemble the keys
        columns = []
        for entry in self.data:
            for col in self.data[entry][key]:
                if col not in columns:
                    columns.append(col)
                    
        f = open(filepath, "wb")
        writer = csv.writer(f)
        writer.writerow(["timestamp"] + columns)
        for timestamp, data in self.data.items():
            row = [timestamp]
            for col in columns:
                if col in data[key]: row.append(data[key][col])
                else: row.append(None)
            writer.writerow(row)
        
         
            
         
        