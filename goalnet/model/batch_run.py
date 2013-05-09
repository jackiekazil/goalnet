'''
Created on May 6, 2013

@author: dmasad

Code to execute batch runs.

Modify as needed for each particular set of experiments, and add comments 
accordingly.

'''

from world import World

'''
Pass 3 - Evening May 07
----------------------------

Agent count = 400 is taking far too long. Reducing and running many more.

max_clock is agent_count
set the data collector to run once every agent_count/50 timesteps.

Will be executed in parallel manually via the terminal.
* * * 
'''
num_runs = 4 # Number of runs per combination
agent_counts = [200, 300]
for count in agent_counts:
    config = {"initial_configuration": "Random1",
              "agent_count": count,
              "max_clock": count * 4,
              "collection_intervals": count/50
              }
    print "New Run:", count
    w = World(config)
    w.init_schedules()
    while w.tick() is not None:
        if w.clock % 10 == 0: print w.clock
    w.data_collector.export()
print "Done!"

'''
End Pass 3
----------
'''



'''
Pass 2 - Morning May 07
----------------------------

Previous runs stalled out at agent_count==400.
Attempting to restart and pick up from there.

max_clock is agent_count
set the data collector to run once every agent_count/50 timesteps.

Will be executed in parallel manually via the terminal.
* * * 
num_runs = 1 # Number of runs per combination
agent_counts = [400, 500]

for count in agent_counts:
    config = {"initial_configuration": "Random1",
              "agent_count": count,
              "max_clock": count * 2,
              "collection_intervals": count/50
              }
    print "New Run:", count
    w = World(config)
    w.init_schedules()
    while w.tick() is not None:
        if w.clock % 10 == 0: print w.clock
    w.data_collector.export()
print "Done!"

End Pass 2
----------
'''


'''
Pass 1 - night of May 06/07
----------------------------
max_clock is agent_count * 2
set the data collector to run once every agent_count/50 timesteps.

Will be executed in parallel manually via the terminal.
* * * 

num_runs = 1 # Number of runs per combination
agent_counts = [50, 100, 200, 300, 400, 500]

for count in agent_counts:
    config = {"initial_configuration": "Random1",
              "agent_count": count,
              "max_clock": count * 2,
              "collection_intervals": count/50
              }
    print "New Run:", count
    w = World(config)
    w.init_schedules()
    while w.tick() is not None:
        if w.clock % 50 == 0: print w.clock
    w.data_collector.export()
print "Done!"

End Pass 1
----------
'''
