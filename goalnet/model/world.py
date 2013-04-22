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
    The model's main world object; runs the simulation and holds its state.
    
    
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
    
    NOTES
    -----
    Scheduling model:
        The model proceeds in terms of 'events', which are simply function
        calls; primarily agent activations and task generation/assignment.
        Each event is associated with a timestamp on the abstracted model clock.
        Events are called in order of their timestamps, while the model's clock
        is set to the timestamp of the most recent event. For example, if the
        event queue was [(1, A), (1.5, B), (2.1 C)] then event A would occur
        at time 1, event B at time 1.5 and event C at time 2.1.
        
        Once an event occurs, it is immediately rescheduled; for example, an
        agent will be activated, and the model will assign a timestamp for that
        agent's next activation. The intervals between activations are drawn 
        from a Poisson-like log-uniform distribution, scaled by a speed factor;
        the higher the speed, the smaller the intervals between occurances.
        
        More formally, let us say that event j will occur at times 
        $t_{j,0}, t_{j,1}...,t_{j,n}$ then:
            $t_{j,n+1} = t_{j,n} + (-1/speed_j)*ln(U[0,1])$
            where U[0,1] is a random variable drawn from a uniform distribution
            between 0 and 1.
        
    '''
    
    def __init__(self, config = {}):
        '''
        Initiate a new model.
        
        Args:
        config: A dictionary containing all (or some of) the model
        configuration parameters, as follows:
            
            "agent_count": How many agents to initiate the model with
            "initial_configuration": How to start off the network
                "None": No connections between agents (default)
                "Random1": For each agent, connect to another random agent
                TODO: Add the rest
            "agent_speed": Scaling factor for scheduling; defaults to 1.
            "task_speed": How often new tasks are assigned; defaults to 1
            "max_clock": The maximum clock tick to run until
        '''
        
        self.agent_count = config["agent_count"]
        self.network = nx.Graph()
        self.agents = {}
        for agent_id in range(self.agent_count):
            pth = random.random()
            cent = random.random()
            greed = random.random()
            self.agents[agent_id] = Agent(agent_id, self, pth, cent, greed)
        
        if config["initial_configuration"] == "None":
            for agent_id in self.agents:
                self.network.add_node(agent_id)
        elif config["initial_configuration"] == "Random1":
            for agent_id in self.agents:
                self.random_new_neighbor(agent_id)
                
                
        
        self.agent_speed = 1
        if "agent_speed" in config:
            self.agent_speed = config["agent_speed"]
        self.task_speed = 1
        if "task_speed" in config:
            self.task_speed = config["task_speed"]
        
        self.max_clock = None 
        if "max_clock" in config:
            self.max_clock = config["max_clock"]
        
        
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
    
    def random_new_neighbor(self, name):
        '''
        Get the specified agent a new neighbor at random.
        
        Updates the agent's network list and the overall network object. 
        '''
        possible_neighbors = [agent_id for agent_id in self.agents
                              if agent_id != name and  
                              not self.network.has_edge(agent_id, name)]
        if possible_neighbors == []:
            return None
        
        neighbor = random.choice(possible_neighbors)
        self.agents[name].network.append(neighbor)
        self.agents[neighbor].network.append(name)
        self.network.add_edge(name, neighbor)
    
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
        
        Tasks are created as follows:
        
        The subtasks parameter is an integer rounded up from a random lognormal 
        distribution, with the properties Min(subtasks)=1, Mode(subtasks)=3
        
        The task payoff is then:
            Payoff = Subtasks + payoff_noise
            where payoff_noise is normally-distributed, with mean=0 and sd=1
        If Payoff < 1, it is coerced to 1.
        
        TODO: have the task parameters change over time. 
        '''
        
        print "Generating task" #Placeholder
        
        # Find out if there are any agents available
        available_agents = [agent for agent in self.agents 
                                if self.agents[agent].task is None]
        if available_agents == []:
            return None
        # Pick the task owner at random
        owner = random.choice(available_agents)
        
        # Subtasks are drawn from an interger log-normal distribution
        subtasks = np.random.lognormal(mean=1, sigma=0.8)
        subtasks = int(np.ceil(subtasks))
        
        # Payoff is number of subtasks + an error
        payoff_noise = np.random.randn()
        payoff = subtasks + payoff_noise
        if payoff <= 1:
            payoff = 1
        
        timeframe = self.agent_speed * 2 # Timeframe fixed for now.
        task_id = len(self.tasks) + 1
        
        new_task = Task(task_id, payoff, subtasks, timeframe, owner)
        self.agents[owner].task = new_task
        self.tasks[task_id] = new_task
        
    
    def tick(self):
        '''
        Advance the model to the next scheduled event.
        
        Calls the next scheduled event, and advances the clock.
        '''
        timestamp, event = heappop(self.queue)
        self.clock = timestamp

        if self.max_clock > 0 and self.clock > self.max_clock:
            return None # End if max time reached.
        
        event()
        
        # Reschedule event:
        if event == self.create_task:
            speed = self.task_speed
        else:
            speed = self.agent_speed
        
        delta = (-1/speed) * np.log(random.random())
        self._add_event(event, self.clock + delta)
        
        return True
    
         
    
    
    
"""
TESTING
=======

Create a new World, with 10 agents, and run until the clock time is 20.
"""

if __name__ == "__main__":
    config = {"agent_count": 10,
              "initial_configuration": "Random1",
              "max_clock": 20}
    w = World(config)
    w.init_schedules()
    while w.tick() is not None:
        print "Network density:", nx.density(w.network)
    
    