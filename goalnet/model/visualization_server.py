'''
A Tornado server that will display the task network as it evolves via a d3.js
page.
'''

import os

import tornado.web
import tornado.websocket
import tornado.ioloop

from networkx.readwrite import json_graph

from world import World


# Model configuration:
model_config = {"initial_configuration": "None",
            "agent_count": 100,
            "max_clock": 100,
            "collection_intervals": 4,
            "task_speed": 1
}



# ================ #
#    HTML PAGE     #
# ================ #

PAGE = '''
<!DOCTYPE html>
<style>
    .link {
        stroke: #999;
        stroke-opacity: 0.6;
    }
</style>
<body>
<script src="http://d3js.org/d3.v3.min.js"></script>
<script src="/static/DynGraph.js"></script>
<script>
    var nodes_received = 0
    var graph = new DynamicGraph("body", 800, 800);
    var last_data;
    var ws = new WebSocket("ws://127.0.0.1:8888/websocket")

    ws.onmessage = function(msg_data) {
        data = JSON.parse(msg_data.data);

        console.log("Got message!")
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
    }
    // Wait for the graph to settle before going again:
    var check_alpha = setInterval(function() {
            if (graph.force.alpha() < 0.05) {
                ws.send("Ready!");
            }
        }, 1000)
    
</script>
Hello World

'''



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
        self.model = World(model_config)
        self.model.init_schedules()
        self.initialize_visualization()
        self.run_model()


    def run_model(self):
        '''
        Run the model until reaching a data collection point.
        '''
        while True:
            self.model.tick()
            if self.model.clock % 2 == 0 and self.model.clock > 0:
                break
        print self.model.clock
        self.send_update()

    def on_message(self, message):
        '''
        When the browser sends a Ready message
        '''
        print message
        self.run_model()

    def initialize_visualization(self):
        '''
        Send the nodes only.
        '''
        data = json_graph.node_link_data(self.model.network)
        self.write_message(data)


    def send_update(self):
        '''
        Send the current task network to the browser.
        '''
        full_data = self.model.data_collector.data[self.model.clock]
        task_network = full_data["task_network"]
        data = json_graph.node_link_data(task_network)
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
