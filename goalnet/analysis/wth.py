import numpy as np

"""
Source data format
{timestamp:
        {"willingness_to_help": 
                    {source_agent_id: {
                                target_1: WTH,
                                target_2: WTH,
                                ...
                                },
                    source_id2: {
                            ...
                            },
                    ...
        {,
timestamp 2: {...}
...
}
"""

def get_agent_wth_by_ts(data):
    '''
    Calculates the average willingness to help 
    for each agent by timestep. 
    Returns a dictionary of... 
        avg_by_agent[agent][timestep] == average of wth for each timestep
    '''
    avg_by_agent = {}
    # ts == timestamp
    for ts in data:
        ts_wth = data[ts]['willingness_to_help']
        print '############TIME: ', ts 
        for agent in ts_wth:
            print 'Agent: ', agent
            print ts_wth[agent]
            agent_avg = np.mean(ts_wth[agent].values())
            try:
                avg_by_agent[agent][ts] = agent_avg
            except KeyError:
                avg_by_agent[agent] = {}
                avg_by_agent[agent][ts] = agent_avg
    
    return avg_by_agent

def get_agent_wth_avg_all_runs(agent_wth_avgs):
    '''
    Calculates the willingness to help average 
    for a single agent for all runs. 
    Returns a dict of...
        wth_by_agent_all_runs[agent] == average of wth over all runs
    '''
    wth_by_agent_all_runs = {}
    for agent in agent_wth_avgs:
        wth_by_agent_all_runs[agent] = np.mean(agent_wth_avgs[agent].values())
    return wth_by_agent_all_runs



def main():
    pass 


if __name__ == '__main__':
    main()