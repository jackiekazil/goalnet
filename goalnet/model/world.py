'''
Created on Apr 5, 2013

@author: dmasad
'''

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
    
    def __init__(self, name):
        '''
        Initiate a new agent.            
        '''
        self.name = name
        self.inbox = []
        self.task = []
        #TODO: Everything else
    
    def get_message(self, source, message):
        '''
        Receive a message from another agent.
        
        Args:
            source: The name of the agent sending the message
            message: A message object to be added to the inbox
        '''
        #TODO: Figure this out; this is just a placeholder
        self.inbox.append((source, message))
    
    
    
    
        
    