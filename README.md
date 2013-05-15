Goalnet
=======

Goalnet is an ABM written in Python that attempts to model informal social and economic coordination frequently occurs across networks, with the shape of the network both shaping the interactions and being shaped by them. 


### To run the model

#### Install requirements:
```
pip install -r requirements.txt
```
* Note: These requirements include numpy & matplotlib, which sometimes can be more involved in setting up, depending on your system. Please contact us if you have issues. 

#### Execute batch run
```
cd goalnet/model/
# edit batch_run.py for the params you wish to set
python batchrun.py
```
* Output will be written to the output folder

### To run the visualization server
```
cd goalnet/model/
python visualization_server.py
```
