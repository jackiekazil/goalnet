'''
Created on Apr 5, 2013
Last updated Apr 13, 2013

@author: dmasad, snayar
'''
import random as r
from collections import namedtuple

Message = namedtuple('Message', ['sender', 'receiver', 'timestamp',
                                 'type', 'data'])

class Agent(object):
    
    '''
    The basic agent class.
    
    This agent attempts to accomplish its Tasks by communicating with other
    agents it is connected with. More description will go here as we build it.
    
    Attributes:
        name: The agent's unique identifier.
        inbox: A lis(?) that holds the agents' messages received
        ... more attributes will go here.
    '''
    
    world = None # World object for all agents in a model
    
    def __init__(self, name):
        '''
        Initiate a new agent.            
        '''
        self.name = name
        self.inbox = [] #where msgs are received from others
        self.task = None
        self.turns = 0  #keep track of how many turns an agent has had
        self.history = []   #keep track of history, who worked with and what payoff received, potentially how the ego felt about the payoff
        self.network = []   #all the other agents in the ego's network
        self.wealth = 0 #This could be the cumulative payoffs
        self.riskthreshold = r.uniform[0,1] #randomly assign a risk threshold for now
        #TODO: Everything else
    
    def activate(self):
        '''
        The agent's sequence of actions each activation.
        
        The sequence is:
            a. Evaluate each message in the inbox
            b. Choose an action:
                i.   Communicate
                ii.  Act on a task
                iii. Seek out new connections
            c. Receive / Distribute payoffs
        '''
        
        for message in self.inbox:
            self.evaluate_message(message)
        
        action = self._choose_action()
        
        if action == 'COMMUNICATE':
            #send a message to another agent in network
            world.agents[r.choice(self.network)].get_message('comm')
        elif action == 'ACT':
            #take action
        elif 'SEEK':
            #look for an introduction from another agent in network
            world.agents[r.choice(self.network)].get_message('seek')
        else:
            #error, this condition should not occur at this time
        
    
    def _choose_action(self):
        '''
        Choose an action to take this turn.
        '''
        #TODO: Fill in.
        actions = ['COMMUNICATE', 'ACT', 'SEEK']
        return r.choice(actions)
    
        
        
        
    
    '''
    MESSAGE HANDLING
    ================
    '''
    
    def get_message(self, message):
        '''
        Receive a message from another agent.
        
        Args:
            message: A message object to be added to the inbox
        '''
        #TODO: Figure this out; this is just a placeholder
        self.inbox.append(message)
        #Show that the message was received
        print self.name,message
    
    def evaluate_message(self, message):
        '''
        Process a given message in the inbox.
        
        '''
        #TODO Fill in action based on message type.
        if message.type == 'HelpRequest':
            self.process_help_request(self, message)
        elif message.type == 'ContactRequest':
            self.process_contact_request(self, message)
        elif message.type == 'Acknowledgment':
            self.process_acknowledgement(self, message)
        elif message.type == 'Payoff':
            self.process_payoff(self, message)
        
        
    def send_message(self, message):
        '''
        Send a message to another agent.
        
        Args:
            message: A message object to be sent to an agent in the ego's network
        '''
        #TODO: Construct a message object and return that
        
        return message
    
    
    def process_help_request(self, message):
        #check to see if ego can help
        #send an acknowledgement to the sender
        
        
    def process_contact_request(self, message):
        #select an agent from ego network
        
    def process_acknowledgement(self, message):
        #process the acknowledgement by sending a message back to the sender
        
    def process_payoff(self, message):
        #record the payoff in ego's history

    