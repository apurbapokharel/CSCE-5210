import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.flow import edmonds_karp
import random
import sys
import numpy as np

class Graph:
    def __init__(self, no_of_nodes, connectivity, seed = 1000):
        self.graph=nx.gnp_random_graph(no_of_nodes, connectivity, seed, True)  

        print("CONNECTION", nx.is_weakly_connected(self.graph))

        for u, v in self.graph.edges():
            capacity=random.randint(1,10)
            flow=random.randint(1,capacity)
            # print('u- v flow - capacity', u, v, flow,capacity)
            self.graph.add_edges_from([(u, v, {'flow':flow }), (u, v,{'capacity': capacity})])
        
        self.graph_flow_edges = nx.get_edge_attributes(self.graph, "flow")
        self.graph_capacity_edges = nx.get_edge_attributes(self.graph, "capacity")
        self.no_of_nodes = self.graph.number_of_nodes()
        path_iterator = nx.all_simple_edge_paths(self.graph, source=0, target=no_of_nodes - 1, cutoff=9)
        self.path = []
        for p in path_iterator:
            self.path.append(p)


    # search_tuple is made of nodes. 
    # (1, 2) represents the tuple of node 1 and node 2
    def getEdgeFlowAndCapacity(self, search_tuple):
        flow = -1
        capacity = -1
        for key in self.graph_flow_edges:
            if key == search_tuple:
                flow = self.graph_flow_edges[key]
                capacity = self.graph_capacity_edges[key]
        return (flow, capacity)
    
    # where u and v are nodes
    def updateFlow(self, u, v, new_flow, capacity):
        self.graph.add_edges_from([(u, v, {'flow': new_flow}), (u, v,{'capacity': capacity})])
        self.graph_flow_edges = nx.get_edge_attributes(self.graph, "flow")

    def getNumberOfNodes(self):
        return self.no_of_nodes

    def plotGraph(self):
        links = [(u, v) for (u, v, d) in self.graph.edges(data=True)]
        pos = nx.drawing.nx_agraph.graphviz_layout(self.graph)
        nx.draw_networkx_nodes(self.graph, pos, node_size=1200, node_color='lightblue', linewidths=0.25) # draw nodes
        nx.draw_networkx_edges(self.graph, pos, edgelist=links, width=4)                                 # draw edges
        nx.draw_networkx_labels(self.graph, pos, font_size=20, font_family="sans-serif")                 # node labels
        edge_labels = nx.get_edge_attributes(self.graph, 'flow')                                         # edge weight labels
        print('edge labels', edge_labels)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels)
        plt.show()

    def simulateGraph(self):
        self.graph = nx.DiGraph()
        self.graph.add_edges_from([(0, 1, {'flow': 2}), (0, 1,{'capacity': 6}),
            (0, 2,{'flow': 3}), (0, 2,{'capacity': 3}),
            (0,3,{'flow': 4}), (0,3,{'capacity': 5}),
            (1,2, {'flow': 1}), (1,2,{'capacity': 5}),
            (1,5, {'flow': 1}), (1,5,{'capacity': 3}),
            (2,4, {'flow': 2}), (2,4,{'capacity': 9}),
            (2,5, {'flow': 4}), (2,5,{'capacity': 8}),
            (3,2, {'flow': 2}), (3,2,{'capacity': 2}),
            (3,4,{'flow': 2}), (3,4,{'capacity': 3}),
            (4,5, {'flow': 4}), (4,5,{'capacity': 5})])
      
        self.graph_flow_edges = nx.get_edge_attributes(self.graph, "flow")
        self.graph_capacity_edges = nx.get_edge_attributes(self.graph, "capacity")
        self.no_of_nodes = self.graph.number_of_nodes()
        path_iterator = nx.all_simple_edge_paths(self.graph, source=0, target=5, cutoff=9)
        self.path = []
        for p in path_iterator:
            self.path.append(p)

    

class Agent:
    def __init__(self, no_of_nodes, connectivity, seed = 1000):
        self.graph = Graph( no_of_nodes, connectivity, seed = 1000)
        # self.graph.simulateGraph()
        self.graph.plotGraph()
        print('graph no of nodes', self.graph.getNumberOfNodes())


    def heuristicFunction(self):
        # 1. calculate the heuristic value for each path and store in heuristic_value_list
        # Nodes make up edges and collection of nodes make up path so,
        # iterate over each path
        heuristic_value_list = []
        for p in self.graph.path:
            minn = sys.maxsize
            # print(p)
            # once inside the path iterate over each edges i.e distance between nodes
            for u,v in p:
                search_tuple = (u,v)
                result_tuple = self.graph.getEdgeFlowAndCapacity(search_tuple)
                remaining_flow = result_tuple[1] - result_tuple[0]
                # print(u,v , remaining_flow)
                if remaining_flow == 0:
                    minn = 0
                    break
                else:
                    minn = min(minn, remaining_flow)
            # print(minn)
            heuristic_value_list.append(minn)
        # 2. find the max heuristic in the heuristic_value_list and resturn the path
        if np.any(heuristic_value_list):
            max_heuristic_index = heuristic_value_list.index(max(heuristic_value_list))
            return (self.graph.path[max_heuristic_index], max(heuristic_value_list))
        else:
            print("all zeross")
            return ()

    def optimizeHeuristic(self, max_heuristic_child_list, increase_factor):
        for u, v in max_heuristic_child_list:
            search_tuple = (u, v)
            result_tuple = self.graph.getEdgeFlowAndCapacity(search_tuple)
            new_flow = result_tuple[0] + increase_factor
            self.graph.updateFlow(u,v, new_flow, result_tuple[1])

    def getOptimizedFlow(self, size = 6):
        sink_node = size - 1
        flow = 0
        for u,v in self.graph.graph_flow_edges:
            if v == sink_node:
                search_tuple = (u, v)
                result_tuple = self.graph.getEdgeFlowAndCapacity(search_tuple)
                flow = flow + result_tuple[0]
        return flow


    def optimize(self):
        # 1. compute the optimized flow using edmonds karp algorithm
        R = edmonds_karp(self.graph.graph, 0, 9)
        flow_value = nx.maximum_flow_value(R, 0, 9) 
        print('OPTIMAL FLOW', flow_value)

        while(1):
            # 2. compute heuristic function on each path
            res = self.heuristicFunction()
           
            # 3. optimize the flow for the chosen path
            if res == ():
                print("Done optimizing")
                break
            else:
                max_heuristic_child_list = res[0]
                heuristic = res[1]
                self.optimizeHeuristic(max_heuristic_child_list, heuristic)     

        # 4. once optimized print the optimized flow
        optimised_flow = self.getOptimizedFlow()
        print('optimised flow', optimised_flow)

        # 5. verify the flow with edmonds_karp algorithm
        assert optimised_flow == flow_value
          

        
if __name__ == "__main__":
    agent = Agent(10, 0.2)
    agent.optimize()
    
