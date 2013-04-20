'''
Created on Apr 5, 2013
Last updated Apr 13, 2013

@author: dmasad, snayar
'''
import random as r
from collections import namedtuple

Message = namedtuple('Message', ['sender', 'receiver', 'timestamp', 'type', 'data'])

class Agent(object):
    
    '''
    The basic agent class.
    
    This agent attempts to accomplish its Tasks by communicating with other
    agents it is connected with. More description will go here as we build it.
    
    Attributes:
        name: The agent's unique identifier.
        world: The World (simstate) object
        inbox: A list that holds the agents' messages received
        ... more attributes will go here.
        task: Current task object; defaults to None
        possible_tasks: Tasks other agents requested help on
        turns: How many times the agent has been activated
        history: Keep track of history, who worked with and what payoff 
            received, potentially how the ego felt about the payoff
        network: List of agents with whom this agent can communicate
        wealth: The total cumulative payoff received, less payoff distributed
        risk_threshold: The agent's risk aversion
        
    '''
    
   
    def __init__(self, name, world):
        '''
        Initiate a new agent.            
        '''
        self.name = name
        self.world = world
        self.inbox = [] #where msgs are received from others
        self.task = None
        self.possible_tasks = []
        self.turns = 0  #keep track of how many turns an agent has had
        self.history = []   #
        self.task_team = []
        self.network = []
        
        #Make sure a connection is not made to self
        neighbor = int(r.random()*10)
        while neighbor == self.name:
            neighbor = int(r.random()*10)
            
        self.network.append(neighbor) #for every agent for now, append a random agent to its network
        self.wealth = 0 #This could be the cumulative payoffs
        self.risk_threshold = r.random() #randomly assign a risk threshold
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
        self.turns += 1
        for message in self.inbox:
            self.evaluate_message(message)
        
        action = self._choose_action()
        print self.name, action
        
        if action == 'COMMUNICATE':
            #send a message to another agent in network
            #TODO
            for eachNeighbor in self.network:
                #create new Message object
                if self.task is not None:
                    message = Message(self.name, eachNeighbor, self.world.clock,'HelpRequest', self.task.task_id)
                else:   #ask for introduction
                    message = Message(self.name, eachNeighbor, self.world.clock,'ContactRequest', None)
                self.world.agents[eachNeighbor].get_message(message)
                  
        elif action == 'ACT':
            #take action
            self.choose_task()
        elif action == 'SEEK':
            #look for an introduction from another agent in network
            self.network.append(self.world.make_random_connection(self.name))
        else:
            #error, this condition should not occur at this time
            pass
        
    
    def _choose_action(self):
        '''
        Choose an action to take this turn.
        '''
        #TODO: Fill in.
        actions = ['COMMUNICATE', 'ACT', 'SEEK']
        return r.choice(actions)
    
        
    def choose_task(self):
        #if self task exists then decide to do that or select a task from the possible tasks
        if self.task:
            self.task.execute_subtask(self.world.clock)
        elif self.possible_tasks != []:
            chosen_task_id = r.choice(self.possible_tasks)
            #remove chosen_task from the list of possible_tasks
            chosen_task = self.world.tasks[chosen_task_id]
            chosen_task.execute_subtask(self.world.clock)
            message = Message(self.name, chosen_task.owner, self.world.clock, 'Acknowledgment',chosen_task_id)
            self.world.agents[chosen_task.owner].get_message(message)
    
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
        print self.name, "got message:", message
        self.inbox.append(message)
        #Show that the message was received
        print self.name,message
    
    def evaluate_message(self, message):
        '''
        Process a given message in the inbox.
        
        '''
        #TODO Fill in action based on message type.
        if message.type == 'HelpRequest':
            self.process_help_request(message)
        elif message.type == 'ContactRequest':
            self.process_contact_request(message)
        elif message.type == 'Acknowledgment':
            self.process_acknowledgement(message)
        elif message.type == 'Payoff':
            self.process_payoff(message)
        
        
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
        task_id = message.data
        self.possible_tasks.append(task_id)
          
        
    def process_contact_request(self, message):
        #select an agent from ego network and add it to the network of the requestor
        self.world.agents[message.sender].network.append(r.choice(self.network))
        
    def process_acknowledgement(self, message):
        #process the acknowledgement by sending a message back to the sender
        self.task_team.append(message.sender)
        if self.task.subtasks == len(self.task.subtasks_executed): #task is complete
            #TODO: calculate payoff to send to others
            other_payoff = 1
            #TODO: accumulate own payoff in wealth
            own_payoff = 1
            self.wealth += own_payoff
            #send the payoff message to each member on the team with the payoff
            for eachMember in self.task_team:
                message = Message(self.name, eachMember, self.world.clock, 'Payoff', other_payoff) #May want to add task id so that the receiver can tell what the payoff was for
                self.world.agents[eachMember].get_message(message)
            
    def process_payoff(self, message):
        #record the payoff in ego's history
        payoff_tuple = message.sender,message.data
        self.history.append(payoff_tuple)
        self.wealth += message.data

    