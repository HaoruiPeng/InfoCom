import socket
import sys

drone_address = "192.168.0.106"
# Bind the socket to the port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (drone_address, 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

while True:
    try:
        # Send data
        message = input("Please input your destination address: ")
        print('Set destination {!r}'.format(message))
        sock.sendall(message.encode())

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        # while amount_received < amount_expected:
        data = sock.recv(64)
        amount_received += len(data)
        print('received {!r}'.format(data.decode()))
    except e:
        print(e)
        print('fail to send destination, try again...')
