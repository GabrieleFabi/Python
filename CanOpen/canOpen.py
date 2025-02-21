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
    network.connect(interface='kvaser', channel=0, bitrate=500000)

    # This will attempt to read an SDO from nodes 1 - 127
    network.scanner.search()
    # We may need to wait a short while here to allow all nodes to respond
    time.sleep(0.05)
    for node_id in network.scanner.nodes:
        print(f"Found node {node_id}!")

    """
    # Read and print messages from the network for 1 second
    start_time = time.time()
    while time.time() - start_time < 1:
        message = network.bus.recv(1.0)  # Timeout after 1 second
        if message:
            print(f"Received message: {message}")
            # Decode the message
            decoded_message = decode_message(message)
            print(f"Decoded message: {decoded_message}")
        else:
            print("No message received within timeout period")
    """

    node = network.add_node(113, 'C:/Users/g.fabi/Test/CanOpen/eds_data.eds')
    network.send_message(0x18BC7148, b'CAN OPEN') #messaggio per cambiare protocollo di comunicazione
    
    # Access the object dictionary entry with index 0x1018
    obj = node.sdo[0x1018]

    # Print the content of the object dictionary entry
    for subindex in obj:
        print(f"Subindex {subindex}: {obj[subindex].raw}")
        
        
    node.sdo.download(0x6042, 0, b'\x00\x00')
    node.sdo.upload(0x6042, 0)

    

    # Access the Data Type variable inside the message with index 0x6043
    data_type_obj = node.sdo[0x6043]

    # Print the content of the Data Type variable




except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Disconnect from the network
    network.disconnect()

