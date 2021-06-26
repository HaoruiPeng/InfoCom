import socket
import sys
import requests

SERVER_URL = "http://0.0.0.0:5000/status"
drone_address = "192.168.0.106"
# Bind the socket to the port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SerialNumber = '10000000e944bb36'
# Connect the socket to the port where the server is listening
server_address = (drone_address, 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

while True:
    try:
        status = None
        message = input('Press any Key to check drone status')
        with requests.Session() as session:
            params = {'SerialNumber': SerialNumber}
            resp = session.get(SERVER_URL, params=params)
            status = resp.text
        if status == 'Idle':
            message = input("Drone is available. \n Please input your destination address: ")
            if len(message.encode('utf-8')) < 5:
                print("Invalid address, try again")
                sock.flush()
                continue
            print('Set destination {!r}'.format(message))
            sock.sendall(message.encode())

            # Look for the response
            amount_received = 0

            data = sock.recv(1)
            print(data)
            if int(data.decode()):
                print('Drone found address, start delivering ...')
                comfirm_data = sock.recv(64)
                print(comfirm_data.decode())
            else:
                print('Fail find destination. Please comfirm your detination address...')
        elif status == 'Activate':
            print('Drone busy, please try later')
    except Exception as e:
        print(e)
        print('fail to send destination, try again...')
    except KeyboardInterrupt:
        sock.close()
        exit(0)
