'''
SOIB - Manhattan network simulator

TODO
- improve packet generation
- parametrize packet generation
- add packet drop due to TTL and full queue
- add routing algorithms
- calculate output parameters and plot them
- add packet visualisation

'''


import link
import node
import packet
import uuid
import networkx as nx
import matplotlib.pyplot as plt
import random as r
import numpy as np
import time

node_list = []
link_list = []

graph = nx.DiGraph()
pos = {}
labels = {}

ttl = 5
total_packets = 0

rows = 3
columns = 3
size = rows*columns


def getNode(row, column):
    for node in node_list:
        if node.id == "{}:{}".format(row,column):
            return node

def getNodeById(id):
    for node in node_list:
        if node.id == id:
            return node

def getLinks(node):

    node_links = []
    for link in link_list:
        if link.node_to_id == node.id or link.node_from_id == node.id:
           node_links.append(link)
    return node_links

def getShortestPath(source, target):
     return nx.shortest_path(graph, source=source, target=target)


def generatePacket(node, ttl):

    while True:
        destination_node = "{}:{}".format(r.randint(1,rows), r.randint(1, columns))
        if destination_node != node.id:
            break
    route = getShortestPath(node.id, destination_node)
    node.buffer_out.append(packet.Packet(uuid.uuid4(), node.id, destination_node, route, ttl))

def transferPacket(node):
    global total_packets

    if node.buffer_in:
        if node.buffer_in[0].node_to == node.id:
            print("Packet {} received by {}".format(node.buffer_in[0].id, node.id))
            node.buffer_in.pop(0)
            total_packets -= 1
        else:
            node.buffer_out.append(node.buffer_in[0])
            node.buffer_in.pop(0)

    if node.buffer_out:
        node.buffer_out[0].route.pop(0)
        node.buffer_out[0].ttl -= 1
        getNodeById(node.buffer_out[0].route[0]).buffer_in.append(node.buffer_out[0])
        print("{} Packet {} sent to {}".format(node.id, node.buffer_out[0].id, node.buffer_out[0].route[0]))
        node.buffer_out.pop(0)

def printNetwork():
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_labels(graph, pos, labels)
    nx.draw_networkx_edges(graph, pos, arrows=True, connectionstyle='arc3,rad=0.2')
    #plt.show()

for row in range(1, rows + 1):
    for column in range(1, columns + 1):
        node_list.append(node.Node("{}:{}".format(row, column)))

for row in range(1, rows + 1):
    for column in range(1, columns):
        if row % 2 == 1:
            link_list.append(link.Link(uuid.uuid1(), getNode(row, column).id, getNode(row, column + 1).id))
        else:
            link_list.append(link.Link(uuid.uuid1(), getNode(row, column + 1).id, getNode(row, column).id))
    if row % 2 == 1:
        link_list.append(link.Link(uuid.uuid1(), getNode(row, columns).id, getNode(row, 1).id))
    else:
        link_list.append(link.Link(uuid.uuid1(), getNode(row, 1).id, getNode(row, columns).id))



for column in range(1, columns + 1):
    for row in range(1, rows):
        if column % 2 == 0:
            link_list.append(link.Link(uuid.uuid1(), getNode(row, column).id, getNode(row + 1, column).id))
        else:
            link_list.append(link.Link(uuid.uuid1(), getNode(row + 1, column).id, getNode(row, column).id))
    if column % 2 == 0:
        link_list.append(link.Link(uuid.uuid1(), getNode(rows, column).id, getNode(1, column).id,))
    else:
        link_list.append(link.Link(uuid.uuid1(), getNode(1, column).id, getNode(rows, column).id))

# Initialize network graph
for node in node_list:
    node_position = (node.id).split(":")
    graph.add_node(node.id)
    pos[node.id] = (int(node_position[1]) * 100, int(node_position[0]) * -100)
    labels[node.id] = node.id

for link in link_list:
    graph.add_edge(link.node_from_id, link.node_to_id)

printNetwork()

#generatePacket(getNode(1,1), 5)
#print(getNode(1,1).buffer_out[0].node_from, getNode(1,1).buffer_out[0].node_to, getNode(1,1).buffer_out[0].route)

for node in node_list:
    for i in range(0, np.random.poisson(2)):
        if i > node.buffer_max:
            break
        generatePacket(node, ttl)
        total_packets += 1

while True:
    print("Total packets in network {}".format(total_packets))
    for node in node_list:

        transferPacket(node)

    time.sleep(1)
