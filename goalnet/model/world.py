'''
Created on Apr 5, 2013

@author: dmasad
'''

import networkx as nx
from agent import Agent

class World(object):
    '''
    The world, as expressed in a networkx Graph object.
    
    World inherits from Graph, and adds model-specific functionality on top.
    This means that all the usual graph analysis functions can be used directly
    on the World object.
    
    Attributes:
        agent_count: number of agents in the simulation.
        agents: A dictionary of agent objects
        network: The networkx Graph object that represents the connections 
        clock: The current timestamp of the model clock.
        tasks: A dictionary of tasks.
        
    '''
    
    def __init__(self, agent_count, initial_configuration="None"):
        '''
        Initiate a new model.
        
        Args:
            agent_count: How many agents to initiate the model with
            initial_configuration: How to start off the network
                "None" -- No connections between agents
                TODO: Add the rest
        '''
        
        self.agent_count = agent_count
        self.network = nx.Graph()
        self.agents = {}
        for agent_id in range(self.agent_count):
            self.agents[agent_id] = Agent(agent_id)
        
        if initial_configuration == "None":
            for agent_id in self.agents:
                self.network.add_node(agent_id)    
        #TODO: Fill in

        
        
    
    
    
    
        
    