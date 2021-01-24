'''
SOIB - Manhattan network simulator

TODO
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
packet_rate = 0.3
buffer_size = 10
simulation_time = 1000
# type of routing algoritm used: SHORTEST_PATH, LONGEST_PATH, RANDOM,
routing_type = "SHORTEST_PATH"

tick = 0
simulation_ticks = []
loss_array = []
hop_array = []
mean_hop_array = []
delay_array = []
mean_delay_array = []

total_packets = 0
sent_packets = 0
received_packets = 0
dropped_packets = 0
loss_rate = 0


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

def getShortestPath(source, target, algorithm):

    if algorithm == "SHORTEST_PATH":
        return nx.shortest_path(graph, source=source, target=target)
    if algorithm == "LONGEST_PATH":
        paths = nx.all_simple_paths(graph, source=source, target=target)
        return max(paths, key=tuple)
    if algorithm == "RANDOM":
        return next(nx.all_simple_paths(graph, source=source, target=target))

def generatePacket(node, ttl):
    global sent_packets
    global total_packets
    global dropped_packets
    global tick

    while True:
        destination_node = "{}:{}".format(r.randint(1,rows), r.randint(1, columns))
        if destination_node != node.id:
            break
    route = getShortestPath(node.id, destination_node, routing_type)

    if len(node.buffer_out) >= node.buffer_max:
        print("Packet {} dropped due to full buffer".format(uuid.uuid4()))
        dropped_packets += 1
    else:
        node.buffer_out.append(packet.Packet(uuid.uuid4(), node.id, destination_node, route, ttl, tick))
        total_packets += 1
    sent_packets += 1

def transferPacket(node):
    global total_packets
    global received_packets
    global dropped_packets
    global tick

    if node.buffer_in:
        while node.buffer_in[0].ttl <= 0:
            print("Packet {} dropped due to expired TTL".format(node.buffer_in[0].id))
            hop_array.append(node.buffer_in[0].hop)
            node.buffer_in.pop(0)
            total_packets -= 1
            dropped_packets += 1
            if not node.buffer_in:
                break

    if node.buffer_in:
        if node.buffer_in[0].node_to == node.id:
            print("Packet {} received by {}".format(node.buffer_in[0].id, node.id))
            hop_array.append(node.buffer_in[0].hop)
            delay_array.append(tick - node.buffer_in[0].sent_time)
            node.buffer_in.pop(0)
            total_packets -= 1
            received_packets += 1
        else:
            node.buffer_out.append(node.buffer_in[0])
            node.buffer_in.pop(0)

    if node.buffer_out:
        node.buffer_out[0].route.pop(0)
        if len(getNodeById(node.buffer_out[0].route[0]).buffer_in) >= node.buffer_max:
            print("Packet {} dropped due to full buffer".format(node.buffer_out[0].id))
            hop_array.append(node.buffer_in[0].hop)
            dropped_packets += 1
            total_packets -= 1
            node.buffer_out.pop(0)
        else:
            node.buffer_out[0].hop += 1
            getNodeById(node.buffer_out[0].route[0]).buffer_in.append(node.buffer_out[0])
            #print("{} Packet {} sent to {}".format(node.id, node.buffer_out[0].id, node.buffer_out[0].route[0]))
            node.buffer_out.pop(0)

def updateTTL(node):
    for packet in node.buffer_in:
        packet.ttl -= 1

    for packet in node.buffer_out:
        packet.ttl -= 1


def printNetwork():
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_labels(graph, pos, labels)
    nx.draw_networkx_edges(graph, pos, arrows=True, connectionstyle='arc3,rad=0.2')
    plt.show()

for row in range(1, rows + 1):
    for column in range(1, columns + 1):
        node_list.append(node.Node("{}:{}".format(row, column), buffer_size))

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

#generatePacket(getNode(1,1), 5)
#print(getNode(1,1).buffer_out[0].node_from, getNode(1,1).buffer_out[0].node_to, getNode(1,1).buffer_out[0].route)


while tick < simulation_time:
    print("Total packets in network {}".format(total_packets))
    print("Packet loss rate: {} %".format(round(loss_rate, 2)))

    for node in node_list:
        for i in range(0, np.random.poisson(packet_rate)):
            generatePacket(node, ttl)
            total_packets += 1
        transferPacket(node)
        updateTTL(node)

    try:
        loss_rate = dropped_packets / sent_packets * 100
    except(ZeroDivisionError):
        loss_rate = 0

    simulation_ticks.append(tick)
    loss_array.append(loss_rate)

    try:
        mean_hop_array.append(sum(hop_array) / len(hop_array))
    except(ZeroDivisionError):
        mean_hop_array.append(0)

    try:
        mean_delay_array.append(sum(delay_array) / len(delay_array))
    except(ZeroDivisionError):
        mean_delay_array.append(0)
    #time.sleep(1)
    tick += 1


# printNetwork()
# plt.show()

plt.plot(simulation_ticks, loss_array)
plt.show()

plt.plot(simulation_ticks, mean_hop_array)
plt.show()

plt.plot(simulation_ticks, mean_delay_array)
plt.show()