'''
Created on Apr 5, 2013

@author: dmasad, snayar
'''

class Task(object):
    '''
    A task that one or more agents will attempt to perform.
    
    For a task to succeed, a certain number of subtasks must be performed within
    a specified timeframe. At this time, tasks and subtasks are completely abstract: subtasks
    are interchangeable; the number of subtasks is the only important factor. 
    
    Attributes:
        task_id: A unique identifier.
        active: True if the task is yet to be accomplished, otherwise False
        payoff: The payoff once the task is accomplished
        completed: A flag initially set to false. It is set to True once the task is complete.
        workers: A list of agents working on the task
        subtasks: Number of subtasks to be undertaken for the task to succeed
        timeframe: The number of clock ticks from the first subtask to the last
            one for the task to succeed.
        owner: The agent that owns the task and is responsible for paying off all the workers
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
        '''
        start_time = max(self.subtasks_executed) - self.timeframe
        subtasks_allowed = [timestamp for timestamp in self.subtasks_executed
                            if timestamp >= start_time]
        #if enough subtasks have been completed then 0 (False) remain
        if len(subtasks_allowed) >= self.subtasks:
            return False
        else: #return the number of subtasks remaining which is the difference between original number of subtasks and the number done so far
            return self.subtasks - len(subtasks_allowed) 
        
    def is_complete(self):
        '''
        Check if the task has been accomplished.
        
        Returns:
            True if the task is complete,
            False otherwise
        '''
        
        #Return False if not enough subtasks executed
        if len(self.subtasks_executed) < self.subtasks:
            return False
        
        start_time = max(self.subtasks_executed) - self.timeframe 
        subtasks_allowed = [timestamp for timestamp in self.subtasks_executed
                            if timestamp >= start_time]
        #If enough subtasks have been executed in a timely manner then return True, else return False
        if len(subtasks_allowed) >= self.subtasks:
            return True
        else:
            return False

        
        
        