'''
A Tornado server that will display the task network as it evolves via a d3.js
page.
'''

import os
import json

import tornado.web
import tornado.websocket
import tornado.ioloop

import networkx as nx
from networkx.readwrite import json_graph

from world import World


# Model configuration:
model_config = {"initial_configuration": "None",
            "agent_count": 100,
            "max_clock": 200,
            "collection_intervals": 4,
            "task_speed": 16
}



# ================ #
#    HTML PAGE     #
# ================ #

PAGE = '''
<!DOCTYPE html>
<title>GoalNet web interface</title>
<style>
    .link {
        stroke: #999;
        stroke-opacity: 0.6;
    }
    .box {
        border: 1px solid #888;
    }
</style>
<body>
<script src="http://d3js.org/d3.v3.min.js"></script>
<script src="/static/DynGraph.js"></script>
<h1>GoalNet</h1>
<h3>Jacqueline Kazil, David Masad, Sanjay Nayar, Melanie Swartz</h3>
<form>
Number of Agents: <input type="text" id="agentCount"> <br />
Task Assignment Speed <input type="text" id="taskSpeed"> <br />
</form>
<button id="launch" onclick="launch()">Start Model</button>

<h3>Task collaboration network:</h3>
<div align="right" id="clock"></div>
<div class="box" id="graph"></div>

<script>
    var nodes_received = 0
    var graph = new DynamicGraph("#graph", self.innerWidth, 600);
    var data;

    var ws = new WebSocket("ws://127.0.0.1:8888/websocket")

    // When the websocket gets a message:
    ws.onmessage = function(msg_data) {
        data = JSON.parse(msg_data.data);

        // console.log("Got message!")
        if (nodes_received === 0) {
            for (i in data.nodes) { graph.addNode("" + i); }
            nodes_received = 1;
        }
        for (j in data.links) {
            var link = data.links[j];
            src = "" + link.source;
            dest = "" + link.target;
            graph.addLink(src, dest, "1");
        }

        // Set the clock:
        document.getElementById("clock").innerHTML = data.clock;   
    
        // Wait for the graph to settle before going again:
        var check_alpha = setInterval(function() {
                var alpha = graph.force.alpha();
                //console.log(alpha);
                if (alpha < 0.05) {
                    ws.send("Ready!");
                    clearInterval(check_alpha);
                }
            }, 1000)
    }

    var launch = function() {
        var agentCount = parseInt(document.getElementById('agentCount').value);
        var taskSpeed = parseInt(document.getElementById('taskSpeed').value);
        if ((!isNaN(agentCount)) && (!isNaN(taskSpeed))) {
            var output = JSON.stringify({"agent_count": agentCount, 
                                         "task_speed": taskSpeed});
            ws.send(output);

            // Disable the button and forms:
            document.getElementById('agentCount').disabled = 'disabled';
            document.getElementById('taskSpeed').disabled = 'disabled';
            document.getElementById('launch').disabled = 'disabled';


        }

    }
</script>
<i>GoalNet + Tornado + d3.js</i> 

'''

# ================ #
#   HELPER FUNCS   #
# ================ #

def compare_graphs(G_old, G_new):
    '''
    Return a graph with only edges that are only new in G_new.
    '''

    G_out = nx.DiGraph()
    for src, dest in G_new.edges():
        if src not in G_old or dest not in G_old[src]:
            G_out.add_edge(src, dest)
    return G_out




# ================ #
#   SERVER CLASS   #
# ================ #

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(PAGE)

class ModelSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        '''
        Called when the browser connects and opens a new websocket.
        '''
        print "Socket open!"
        #self.launch_model(model_config)


    def launch_model(self, config):
        '''
        Launch the model with the given config dictionary.
        '''
        self.last_network = None
        self.model = World(config)
        self.model.init_schedules()
        self.initialize_visualization()
        self.run_model()
    
    def run_model(self):
        '''
        Run the model until reaching a data collection point.
        '''
        if self.model.clock > self.model.max_clock:
            return None

        while True:
            self.model.tick()
            if self.model.clock % 2 == 0 and self.model.clock > 0:
                break
        #print self.model.clock
        self.send_update()

    def on_message(self, message):
        '''
        When the browser sends a Ready message
        '''
        #print message
        if message == "Ready!":
            self.run_model()
        else:
            params = json.loads(message)
            config = {"initial_configuration": "None",
                        "agent_count": params['agent_count'],
                        "max_clock": params['agent_count'] * 2,
                        "collection_intervals": 4,
                        "task_speed": params['task_speed']}
            self.launch_model(config)

    def initialize_visualization(self):
        '''
        Send the nodes only.
        '''
        data = json_graph.node_link_data(self.model.network)
        data['clock'] = 0
        self.write_message(data)


    def send_update(self):
        '''
        Send the updates to the task network to the browser.
        '''
        full_data = self.model.data_collector.data[self.model.clock]
        

        if "task_network" not in full_data:
            return None

        task_network = full_data["task_network"]
        if self.last_network is not None:
            out_graph = compare_graphs(self.last_network, task_network)
        else:
            out_graph = task_network
        self.last_network = task_network

        #data = json_graph.node_link_data(task_network)
        data = json_graph.node_link_data(out_graph)
        data = {'links': data["links"], 'clock': self.model.clock}
        self.write_message(data)

        #self.run_model() # Go back to running the model.


    def on_close(self):
        print "Socket closed!"


if __name__ == "__main__":

    app = tornado.web.Application([
            ("/", MainHandler),
            #("/DynGraph.js", tornado.web.StaticFileHandler, {"path": "DynGraph.js"}),
            ("/static/(.*)", tornado.web.StaticFileHandler, 
                {"path": os.path.join(os.path.dirname(__file__), 'static')}),
            ("/websocket", ModelSocket)
        ],)
    app.listen(8888)
    main_loop = tornado.ioloop.IOLoop.instance().start()
