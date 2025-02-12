import canopen
import time

# Create a network object
network = canopen.Network()

# Connect to the network
network.connect(interface='kvaser', channel=0, bitrate=500000)

# This will attempt to read an SDO from nodes 1 - 127
network.scanner.search()
# We may need to wait a short while here to allow all nodes to respond
time.sleep(0.05)
for node_id in network.scanner.nodes:
    print(f"Found node {node_id}!")

node = network.add_node(113, 'C:/Users/g.fabi/Test/CanOpen/eds_data.eds')  

network.send_message(0x18BC7148, b'CAN OPEN') #messaggio per cambiare protocollo di comunicazione