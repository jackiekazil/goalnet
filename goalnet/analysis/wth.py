import numpy as np


def get_agent_wth_avg(data):
    '''
    Calculates the average willingness to help 
    for each agent by timestep. 
    Returns a dictionary of... 
        wtf_by_agent[agent][timestep] == average of wth for each timestep
    '''

    wth_by_agent = {}
    for agent in data:
        wth_by_agent[agent] = {}
        for timestep in data[agent]['willingness_to_help']:
            t_avg = np.mean(data[agent]['willingness_to_help'][timestep].values())
            wth_by_agent[agent][timestep] = t_avg

    return wth_by_agent

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