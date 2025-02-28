import canopen
import time

# Create a network object
network = canopen.Network()

def decode_message(message):
    # Example decoding function
    # This function should be customized based on the specific message structure
    decoded = {
        'id': message.arbitration_id,
        'data': message.data.hex(),
        'timestamp': message.timestamp
    }
    return decoded

try:
    # Connect to the network
    network.connect(interface='kvaser', channel=0, bitrate=250000)

    # This will attempt to read an SDO from nodes 1 - 127
    network.scanner.search()
    # We may need to wait a short while here to allow all nodes to respond

   

    node = network.add_node(113, 'C:/Users/g.fabi/Test/CanOpen/eds_data.eds')
    network.send_message(0x18BC7148, b'CAN OPEN') #messaggio per cambiare protocollo di comunicazione

    obj = node.object_dictionary[0x1000]
    print(obj)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Disconnect from the network
    network.disconnect()

