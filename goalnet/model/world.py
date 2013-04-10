'''
Created on Apr 5, 2013

@author: dmasad
'''

from __future__ import division

# Standard library imports
import random
from heapq import heappush, heappop
from math import log

# Other packages
import numpy as np
import networkx as nx

# Model imports
from agent import Agent
from task import Task

class World(object):
    '''
    The world, as expressed in a networkx Graph object.
    
    World inherits from Graph, and adds model-specific functionality on top.
    This means that all ^the usual graph analysis functions can be used directly
    on the World object.
    
    Attributes:
        Parameters
        ----------
        agent_count: number of agents in the simulation.
        
        
        Data Structures
        ---------------
        agents: A dictionary of agent objects
        network: The networkx Graph object that represents the connections 
        tasks: A dictionary of tasks.
        
        Scheduling
        ----------
        queue: A queue of functions to call
        clock: The current timestamp of the model clock.
        agent_speed: The mean interval of agent activation
        task_speed: The mean interval of task generation

    '''
    
    def __init__(self, config = {}):
        '''
        Initiate a new model.
        
        Args:
        config: A dictionary containing all (or some of) the model
        configuration parameters, as follows:
            
            "agent_count": How many agents to initiate the model with
            "initial_configuration": How to start off the network
                "None" -- No connections between agents
                TODO: Add the rest
            "agent_speed": Scaling factor for scheduling; defaults to 1.
            "task_speed": How often new tasks are assigned; defaults to 1
        '''
        
        self.agent_count = config["agent_count"]
        self.network = nx.Graph()
        self.agents = {}
        for agent_id in range(self.agent_count):
            self.agents[agent_id] = Agent(agent_id)
        
        if config["initial_configuration"] == "None":
            for agent_id in self.agents:
                self.network.add_node(agent_id)
        
        self.agent_speed = 1
        if "agent_speed" in config:
            self.agent_speed = config["agent_speed"]
        self.task_speed = 1
        if "task_speed" in config:
            self.task_speed = config["task_speed"]
        
        
        self.clock = 0
        self.queue = []
        
        self.tasks = {}
            
        #TODO: Fill in additional config
    
    def _add_event(self, event, timestamp):
        '''
        Adds an event to the queue at the given timestamp.
        
        Args:
            event: A function to be called.
            timestamp: The timestamp to call the event at.
        '''
        heappush(self.queue, (timestamp, event))
        
    
    def init_schedules(self, agent_delay = 0):
        '''
        Schedule the initial activation for all agents and tasks.
        
        Args:
            agent_delay: A clock time to delay the agent activation; allows 
            some tasks to be assigned before agents begin to be active. 
        '''
        
        timestamp = (-1/self.task_speed) * np.log(random.random())
        self._add_event(self.create_task, timestamp)
        
        for agent in self.agents.values():
            timestamp = (-1/self.agent_speed) * np.log(random.random())
            timestamp += agent_delay
            self._add_event(agent.activate, timestamp)
        
    
    def create_task(self):
        '''
        Create a new task and assign it to an agent.
        
        Currently, the task parameters are constant.
        TODO: have the task parameters change over time. 
        '''
        
        # Subtasks are drawn from an interger log-normal distribution
        subtasks = np.random.lognormal(mu=1, sigma=0.8)
        subtasks = int(np.ceil(subtasks))
        
        # Payoff is number of subtasks + an error
        payoff_noise = np.random.randn()
        payoff = subtasks + payoff_noise
        if payoff <= 1:
            payoff = 1
        
        timeframe = self.agent_speed * 2 # Timeframe fixed for now.
        task_id = len(self.tasks) + 1
        
        new_task = Task(task_id, payoff, subtasks, timeframe)
        
        owner = random.choice(self.agents.values())
        while owner.task is not None:
            owner = random.choice(self.agents.values())
        owner.task = new_task
    
    def tick(self):
        '''
        Advance the model to the next scheduled event.
        
        Calls the next scheduled event, and advances the clock.
        '''
        timestamp, event = heappop(self.queue)
        self.clock = timestamp
        event()
        
        # Reschedule event:
        if event == self.create_task:
            speed = self.task_speed
        else:
            speed = self.agent_speed
        
        delta = (-1/speed) * np.log(random.random())
        self._add_event(self.event, self.clock + delta)
        
        
        
        
        
        
                    
            
        
        
        
        
    
    
        
        
    
    

    
    
        
    
    
    
    
        
    