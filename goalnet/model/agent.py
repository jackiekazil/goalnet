'''
Created on Apr 5, 2013

@author: dmasad
'''
import random
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
        self.inbox = []
        self.task = None
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
        
    
    def _choose_action(self):
        '''
        Choose an action to take this turn.
        '''
        #TODO: Fill in.
        actions = ['COMMUNICATE', 'ACT', 'SEEK']
        return random.choice(actions)
    
        
        
        
    
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
    
    def evaluate_message(self, message):
        '''
        Process a given message in the inbox.
        
        '''
        #TODO Fill in action based on message type.
        if message.type == 'HelpRequest':
            pass
        elif message.type == 'ContactRequest':
            pass
        elif message.type == 'Acknowledgment':
            pass
        elif message.type == 'Payoff':
            pass
        
        
    
    