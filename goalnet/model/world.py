'''
Created on Apr 5, 2013

@author: dmasad
'''

import networkx as nx

class World(nx.Graph):
    '''
    The world, as expressed in a networkx Graph object.
    
    World inherits from Graph, and adds model-specific functionality on top.
    This means that all the usual graph analysis functions can be used directly
    on the World object.
    
    Attributes:
        clock: the current timestamp of the model clock.
        tasks: A dictionary of tasks.
    '''
    
    
    
    
        
    