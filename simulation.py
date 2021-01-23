import packet
import link
import node
import uuid
import networkx as nx
import matplotlib.pyplot as plt

node_list = []
link_list = []

graph = nx.DiGraph()
pos = {}
labels = {}

rows = 4
columns = 4
size = rows*columns

def getNode(row, column):
    for node in node_list:
        if node.id == "{}:{}".format(row,column):
            return node

def getLinks(node):

    node_links = []
    for link in link_list:
        if link.node_to_id == node.id or link.node_from_id == node.id:
           node_links.append(link)
    return node_links


for row in range(1, rows + 1):
    for column in range(1, columns + 1):
        node_list.append(node.Node("{}:{}".format(row,column)))



for row in range(1, rows + 1):
    for column in range(1, columns):
       link_list.append(link.Link(uuid.uuid1(), getNode(row, column).id, getNode(row, column + 1).id, "Uplink"))
       #print(getNode(row, column).id)
    link_list.append(link.Link(uuid.uuid1(), getNode(row, columns).id, getNode(row, 1).id, "Uplink"))

for column in range(1, columns + 1):
    for row in range(1, rows):
       link_list.append(link.Link(uuid.uuid1(), getNode(row, column).id, getNode(row + 1, column).id, "Downlink"))
       #print(getNode(row, column).id)
    link_list.append(link.Link(uuid.uuid1(), getNode(rows, column).id, getNode(1, column).id, "Downlink"))



for node in node_list:
    print(node.id)
    for link in getLinks(node):
        print(link.node_from_id, link.node_to_id, link.direction)
    print()


# Draw network
for node in node_list:
    node_position = (node.id).split(":")
    graph.add_node(node.id)
    pos[node.id] = (int(node_position[1]) * 100, int(node_position[0]) * -100)
    labels[node.id] = node.id

for link in link_list:
    graph.add_edge(link.node_from_id, link.node_to_id)



nx.draw_networkx_nodes(graph, pos)
nx.draw_networkx_labels(graph, pos, labels)
nx.draw_networkx_edges(graph, pos, arrows=True, connectionstyle='arc3,rad=0.2')
plt.show()
