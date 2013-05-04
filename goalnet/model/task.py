'''
Created on Apr 5, 2013

@author: dmasad
'''

class Task(object):
    '''
    A task that one or more agents will attempt to perform.
    
    For a task to succeed, a certain number of subtasks must be performed within
    a specified timeframe. At the moment, this is completely abstract: subtasks
    are interchangeable; the number of subtasks is the only important factor. 
    
    Attributes:
        task_id: A unique identifier.
        active: True if the task is yet to be accomplished, otherwise False
        payoff: The payoff once the task is accomplished
        subtasks: Number of subtasks to be undertaken for the task to succeed
        timeframe: The number of clock ticks from the first subtask to the last
            one for the task to succeed.
        subtasks_executed: A list of ticks at which subtasks have been executed.
        
    '''


    def __init__(self, task_id, payoff, subtasks, timeframe, owner = None):
        '''
        Create a new task.
        '''
        self.task_id = task_id
        self.active = True
        self.payoff = payoff
        self.completed = False
        self.workers = []
        self.subtasks = subtasks
        self.timeframe = timeframe
        self.owner = owner
        self.subtasks_executed = []
        
    
    def execute_subtask(self, tick):
        '''
        Record the execution of a subtask at the specified tick
        '''
        
        self.subtasks_executed.append(tick)
    
    
    def get_subtasks_remaining(self):
        '''
        Return an estimate of how many subtasks are needed to complete the task.
        TODO: Why do we need an estimate and not the exact subtasks needed?
        '''
        start_time = max(self.subtasks_executed) - self.timeframe
        subtasks_allowed = [timestamp for timestamp in self.subtasks_executed
                            if timestamp >= start_time]
        if len(subtasks_allowed) >= self.subtasks:
            return False
        else:
            return self.subtasks - len(subtasks_allowed) 
        
    def is_complete(self):
        '''
        Check if the task has been accomplished.
        
        Returns:
            True if the task is complete,
            False otherwise
        '''
        
        if len(self.subtasks_executed) < self.subtasks:
            return False
        
        start_time = max(self.subtasks_executed) - self.timeframe 
        subtasks_allowed = [timestamp for timestamp in self.subtasks_executed
                            if timestamp >= start_time]
        if len(subtasks_allowed) >= self.subtasks:
            return True
        else:
            return False

        
        
        