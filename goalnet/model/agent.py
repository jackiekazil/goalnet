'''
Created on Apr 5, 2013
Last updated Apr 13, 2013

@author: dmasad, snayar
'''
import random
from collections import namedtuple
from task import Task

Message = namedtuple('Message', ['sender', 'receiver', 'timestamp', 'type', 'data'])

class Agent(object):
    
    '''
    The basic agent class.
    
    This agent attempts to accomplish its Tasks by communicating with other
    agents it is connected with. More description will go here as we build it.
    
    Attributes:
        name: The agent's unique identifier.
        world: The World (simstate) object
        
        propensity_to_help: The agent's initial willingness to help others
        centralization: The agent's willingness to share contacts
        greed: The proportion of task payoff an agent is inclined to keep
        beta: The discount factor on past events; currently fixed at 1.
        
        inbox: A list that holds the agents' messages received.Gets cleared by 
               the agent every turn as the contained messages are processed
        task: Current task object; defaults to None
        possible_tasks: Tasks other agents requested help on
        turns: How many times the agent has been activated
        history: Keep track of history, who worked with and what payoff 
            received, potentially how the ego felt about the payoff
        network: List of agents with whom this agent can communicate
        wealth: The total cumulative payoff received, less payoff distributed
        
        Willingness To Help (WTH) model:
        ===============================
            History coding:
            --------------
                Received help from B:    +1.0
                B provides introduction: +0.5
                B DOESN'T provide intro: -1.0
                B provides payoff:
                    (ActualPay - FairPay)/FairPay 
        
    '''
    
   
    def __init__(self, name, world, propensity_to_help, centralization, greed):
        '''
        Initiate a new agent.            
        '''
        self.name = name
        self.world = world
        self.propensity_to_help = propensity_to_help
        self.centralization = centralization
        self.greed = greed
        
        self.inbox = [] #where msgs are received from others
        self.task = None
        self.task_contributors = [] # Agents who have performed subtasks
        self.possible_tasks = []
        self.turns = 0  #keep track of how many turns an agent has had
        
        self.history = []
        self.outstanding_payoffs = {}
        self.beta = 2 # Past discount factor
        
        self.task_team = []
        self.network = []
        
        self.wealth = 0 #This could be the cumulative payoffs
        
            
    def activate(self):
        '''
        The agent's sequence of actions each activation.
        
        The sequence is:
            a. Evaluate each message in the inbox
            b. Choose an action
            c. Receive / Distribute payoffs
        '''
        self.turns += 1
        
    
        # Evaluate messages
        self.possible_tasks = []
        for message in self.inbox:
            self.evaluate_message(message)
        
        # Choose action
        action, target = self._choose_action()
        print self.name, action
        
        # Take action
        if action == 'COMMUNICATE':
            #send a message to another agent in network
            for eachNeighbor in self.network:
                #create new Message object
                if target is not None:
                    message = Message(self.name, eachNeighbor, self.world.clock,
                                      'HelpRequest', self.task.task_id)
                else:   #ask for introduction
                    message = Message(self.name, eachNeighbor, self.world.clock,
                                      'ContactRequest', None)
                self.world.agents[eachNeighbor].get_message(message)
                  
        elif action == 'ACT':
            task = self.world.tasks[target]
            task.execute_subtask(self.world.clock)
            # If working on someone else's task, send them a message.
            if self.task is None or target != self.task.task_id:
                message = Message(self.name, task.owner, self.world.clock,
                                  'Acknowledgment', task.task_id)
                self.world.agents[task.owner].get_message(message)
                self.world.tasks[task.task_id].workers.append(self.name)
                
        elif action == 'SEEK':
            #look for an introduction from another agent in network
            self.world.random_new_neighbor(self.name)
        else:
            #error, this condition should not occur at this time
            pass
        
        # Check to see if task complete; if so, distribute payoffs
        if self.task is not None and self.task.is_complete():
            print "Task %s completed by %s!"% (self.task.task_id, self.name)
            self.task.completed = True
            self.task.workers.append(self.name)
            # Distribute payoffs:
            self.task.active = False
            total_payoff = self.task.payoff
            self.wealth += self.greed * total_payoff
            # Distribute payoffs:
            weights = {}
            total_weights = 0.0
            # Compute relative payoffs:
            for agent in self.task_contributors:
                wth = self._willingness_to_help(agent)
                if wth < 0: wth = 0
                weights[agent] = wth
                total_weights += wth
            
            if total_weights ==0:
                self.wealth += (1-self.greed) * total_payoff
            for agent in self.task_contributors:
                if total_weights == 0:
                    payoff = 0
                else:
                    payoff = (weights[agent]/total_weights)*total_payoff
                message = Message(self.name, agent, self.world.clock, 'Payoff',
                                  (self.task.task_id, payoff))
                self.world.agents[agent].get_message(message)
            self.task = None
               
        self.inbox = [] 
                
            
                
    
    def _willingness_to_help(self, neighbor):
        '''
        Compute agent's Willingness to Help the specified neighbor.
        
        Takes into account both the interactions with that specific agent
        and with all others.
        
        Returns the computed WTH number.
        '''    
        
        neighbor_interactions = 0
        other_interactions = 0
        current_clock = self.world.clock
        
        for event in self.history:
            delta_i = (event[1] / (current_clock - event[2])**self.beta)
            if event[0] == neighbor:
                neighbor_interactions += delta_i
            else:
                other_interactions += delta_i
        #TODO: Why this division?
        other_interactions /= (1.0 * len(self.network))
        #TODO: other_interactions overwhelm neighbor_interactions
        wth = (neighbor_interactions + other_interactions)/2.0
        wth += (self.propensity_to_help / (current_clock)**self.beta)
        return wth  
         
            
    
    def _choose_action(self):
        '''
        Choose an action to take this turn.
        '''
        #TODO: Fill in.
        
        # Build task probabilities
        possible_tasks = {}
        for task_id in self.possible_tasks:
            task = self.world.tasks[task_id]
            owner = task.owner
            wth = self._willingness_to_help(owner)
            fair_pay = (task.payoff * (1.0-self.greed))/task.subtasks
            possible_tasks[task_id] = wth * fair_pay
        
        if self.task is not None:
            possible_tasks[self.task.task_id] = self.task.payoff * self.greed
        elif len(self.possible_tasks) > 0:
            mean_weight = 0
            for w in possible_tasks.values():
                mean_weight += 1
            mean_weight /= (len(possible_tasks)*1.0)
            possible_tasks[None] = mean_weight
            
        # Pick a task based on payoff:
        total = sum(possible_tasks.values())
        choice = self.world.random_number_generator.random() * total
        counter = 0
        result = None
        for key, wgt in possible_tasks.items():
            if choice < counter + wgt: 
                result = key
            else: 
                counter += wgt
        if result in self.possible_tasks:
            return ("ACT", result) #Act on someone else's task
        elif result is not None:
            assert result is self.task.task_id
            if self.task.get_subtasks_remaining == 1:
                return ("ACT", result) # Act on own task
            else:
                return ("COMMUNICATE", result)
        else:
            # If none, decide whether to communicate or seek:
            if self.world.random_number_generator.random() < (1 - self.centralization) and len(self.network) > 2:
                return ("COMMUNICATE", None)
            else:
                return ("SEEK", None)
        
        
        
    
        
    def choose_task(self):
        #if self task exists then decide to do that or select a task from the possible tasks
        if self.task:
            self.task.execute_subtask(self.world.clock)
        elif self.possible_tasks != []:
            chosen_task_id = random.choice(self.possible_tasks)
            #remove chosen_task from the list of possible_tasks
            chosen_task = self.world.tasks[chosen_task_id]
            chosen_task.execute_subtask(self.world.clock)
            message = Message(self.name, chosen_task.owner, self.world.clock, 
                              'Acknowledgment',chosen_task_id)
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
        #print self.name, "got message:", message
        for eachMessage in self.inbox:
            if eachMessage.sender == message.sender and eachMessage.type == message.type and eachMessage.data == message.data:
                break
        else:
            self.inbox.append(message)
    
    def evaluate_message(self, message):
        '''
        Process a given message in the inbox.
        
        '''
        if message.type == 'HelpRequest':
            self.process_help_request(message)
        elif message.type == 'ContactRequest':
            self.process_contact_request(message)
        elif message.type == 'Acknowledgment':
            self.process_acknowledgment(message)
        elif message.type == 'Payoff':
            self.process_payoff(message)
    
    
    def process_help_request(self, message):
        #check to see if ego can help
        task_id = message.data
        if self.name == 6:
            pass
        #print 'Possible Tasks for %s before append %s'% (self.name, self.possible_tasks)
        self.possible_tasks.append(task_id)
        #print 'Possible Tasks for %s after append %s'% (self.name, self.possible_tasks)
          
        
    def process_contact_request(self, message):
        '''
        Optionally introduce the requester to a new neighbor. 
        '''
        source = self.world.agents[message.sender]

        if self.world.random_number_generator.random() > self.centralization: # TODO: Add WTH
            possible_connections = [neighbor for neighbor in self.network
                                        if neighbor != source.name and 
                                        neighbor not in source.network]
            if possible_connections == []: return None
                
            new_connection = self.world.random_number_generator.choice(possible_connections)
            #if new_connection == 3 or new_connection == 4:
            #    print "Agent %s, network before append is %s"% (new_connection, self.world.agents[new_connection].network)
            #    print "Agent %s, network before append is %s"% (source.name, self.world.agents[source.name].network)

            #Update the networks of both the agents
            self.world.agents[new_connection].network.append(source.name)
            self.world.agents[source.name].network.append(new_connection)

            #if new_connection == 3 or new_connection == 4:
            #    print "Agent %s, network after append is %s"% (new_connection, self.world.agents[new_connection].network)
            #    print "Agent %s, network after append is %s"% (source.name, self.world.agents[source.name].network)     
            self.world.network.add_edge(source.name, new_connection)
            # Manually add the event for now
            source.history.append((self.name, 0.5, self.world.clock))
        else:
            source.history.append((self.name, -1.0, self.world.clock))
            
                
    def process_acknowledgment(self, message):
        '''
        Add a history event when another agent works on your task
        '''
        new_event = (message.sender, 1.0, message.timestamp)
        self.history.append(new_event)
        self.task_contributors.append(message.sender)
    
            
    def process_payoff(self, message):
        '''
        Record the payoff received from an agent; increment wealth and history.
        
        The specific increment will be based on fairness.
        '''
        task_id, payoff = message.data # Unpack the tuple
        self.wealth += payoff
        task = self.world.tasks[task_id]
        fair_pay = (task.payoff * (1.0-self.greed))/task.subtasks
        event = 1 + (payoff - fair_pay)/(fair_pay)
        self.history.append((message.sender, event, message.timestamp))
         
        
        
        
        

    