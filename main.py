import random
import networkx as nx
import matplotlib.pyplot as plt


class Intersection:     #intersection class
    def __init__(self, intersection_id):
        self.id = intersection_id
        self.connected_roads = []

    #Add a road to the intersection's list of connected roads
    def add_road(self, road_id):
        self.connected_roads.append(road_id)


class Road:     #road class
    def __init__(self, road_id, road_name, length):
        self.id = road_id
        self.road_name = road_name
        self.length = length

class RoadNetworkGraph:         #road network graph class
    def __init__(self):
        self.intersections = {}
        self.roads = {}
        self.next_road_id = 1

    def add_intersection(self, intersection_id):        #add a new intersection to the graph
        if intersection_id not in self.intersections:
            self.intersections[intersection_id] = Intersection(intersection_id)

    def add_road(self, road_name):  #add a new road to the graph
        road_id = self.next_road_id
        self.next_road_id += 1
        length = random.randint(1, 20)
        self.roads[road_id] = Road(road_id, road_name, length)
        return road_id


    def connect_intersection_to_road(self, intersection_id, road_id):   #connect an intersection to a road
        if intersection_id in self.intersections and road_id in self.roads:
            intersection = self.intersections[intersection_id]
            intersection.add_road(road_id)

    def visualize_graph(self):  #visualize the road network graph
        G = nx.DiGraph()

        for intersection_id in self.intersections:  #add nodes for intersections
            G.add_node(intersection_id)

        for road_id, road in self.roads.items():    #add edges for roads
            for intersection_id in self.intersections:
                if road_id in self.intersections[intersection_id].connected_roads:
                    congestion_level = random.randint(1, 5)
                    G.add_edge(intersection_id, road_id, road_name=road.road_name, length=road.length, congestion=congestion_level)

        #start plotting the graphs of the roads and through vertices, nodes
        plt.figure(figsize=(15, 15))
        pos = nx.spring_layout(G, scale=10)

        edge_labels = {}
        for u, v in G.edges():
            label = G.edges[u, v]['road_name'] + ", ID: ," + str(v) + ",KM: " + str(G.edges[u, v]['length']) + ", Time: " + str(G.edges[u, v]['congestion']) + ")"
            edge_labels[(u, v)] = label

        nx.draw(G, pos, with_labels=True, node_size=400, node_color='skyblue', font_size=7, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color='red')

        plt.title("Road Network Graph")
        plt.show()

    def ensure_vertex_connectivity(self):           #incase of any mistakes occure this code ensures that all intersections are connected to at least one road
        for intersection_id in self.intersections:
            if not self.intersections[intersection_id].connected_roads:
                road_name = f"Bridge {intersection_id}"
                road_id = self.add_road(road_name)
                self.connect_intersection_to_road(intersection_id, road_id)


    def find_shortest_path(self, start_intersection_id, end_intersection_id):       #find the shortest path between two intersections
        G = nx.Graph()

        for road_id, road in self.roads.items():
            for intersection_id in self.intersections:
                if road_id in self.intersections[intersection_id].connected_roads:
                    G.add_edge(intersection_id, road_id, weight=road.length)

        if nx.has_path(G, start_intersection_id, end_intersection_id):
            shortest_path = nx.shortest_path(G, source=start_intersection_id, target=end_intersection_id, weight='weight')
            return shortest_path
        else:
            return None

    def routing_suggestions(self, start_intersection_id, end_intersection_id):      #provide routing suggestions for a given start and end intersection
        shortest_path = self.find_shortest_path(start_intersection_id, end_intersection_id)
        if shortest_path:
            suggestions = []
            for i in range(len(shortest_path) - 1):
                intersection_id = shortest_path[i]
                road_id = shortest_path[i + 1]
                for connected_road_id in self.intersections[intersection_id].connected_roads:
                    if connected_road_id == road_id:
                        road = self.roads[road_id]
                        suggestions.append(road.road_name)
                        break
            return suggestions
        else:
            return None

#instance of the RoadNetworkGraph
road_network = RoadNetworkGraph()

#20 intersections
for i in range(1, 21):
    road_network.add_intersection(i)

#add 9 roads and connect them to intersections randomly
for i in range(1, 10):
    road_name = f"Road {i}"
    road_id = road_network.add_road(road_name)
    for intersection_id in road_network.intersections:
        if random.random() < 0.1:
            road_network.connect_intersection_to_road(intersection_id, road_id)

road_network.ensure_vertex_connectivity()       #Ensure vertex connectivity in the graph

road_network.visualize_graph()      #visualize the road network graph

#find the shortest path between two intersections
start_intersection_id = 1
end_intersection_id = 20

shortest_path = road_network.find_shortest_path(start_intersection_id, end_intersection_id)
if shortest_path:
    print("Shortest Path:", shortest_path)
else:
    print("No path between the intersections.")

#Then provide routing suggestions for the given start and end intersection
suggestions = road_network.routing_suggestions(start_intersection_id, end_intersection_id)
if suggestions:
    print("Routing Suggestions:", suggestions)
else:
    print("No routing suggestions available")
