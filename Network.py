import networkx as nx
import matplotlib.pyplot as plt
import random

up_network = []
color = {"Node_1": "blue", "Node_2": "blue", "Node_3": "blue", "Node_4": "blue"
        , "Node_5": "blue", "Node_6": "blue", "Node_7": "blue", "Node_8": "blue", "Node_9": "blue"
        , "Node_10": "blue", "Sender": "blue", "Receiver": "blue"}
mapping = {0: "Node_1", 1: "Node_2", 2: "Node_3", 3:"Node_4", 4:"Node_5",
           5:"Node_6", 6:"Node_7", 7:"Node_8", 8:"Node_9", 9:"Node_10"}
def connect_party_2_network(): # sender and receiver comes in network and connect to random nodes
    up_network=([e for e in G.nodes])
    node_s = random.choice(up_network)
    node_r = random.choice(up_network)
    if node_s==node_r:
        connect_party_2_network()
    else:
        G.add_edge("Sender",node_s)
        G.add_edge("Receiver",node_r)
        color["Sender"] = "yellow"
        color["Receiver"] = "yellow"
        color[node_s] = "yellow"
        color[node_r] = "yellow"
    return node_r,node_s


# FORMING NETWORK
G = nx.complete_graph(10)
G=nx.relabel_nodes(G, mapping)
node_1,node_2 = connect_party_2_network().

# can pass the choosen nodes as variable to the function too, or simply create a database for the same
# using txt file here as database
f=open("client_1.txt",'w')
f.write(node_1)
f.close()
f=open("client_2.txt",'w')
f.write(node_2)
f.close()
nx.draw_networkx(G, pos=nx.circular_layout(G), node_color= [color[key] for key in color], with_labels = True)
def show_network():
    plt.show()

# show_network()

