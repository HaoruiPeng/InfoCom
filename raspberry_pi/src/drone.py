from geopy.geocoders import Nominatim
import socket
import sys
import numpy as np
import time
import requests

SERVER_URL = "http://192.168.0.150:5000/clock"

def getserialNumber():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
    return cpuserial

def get_directions(src, dst, speed):
    dst_x, dst_y = dst
    x, y = src
    direction = np.sqrt((dst_x - x)**2 + (dst_y - y)**2)
    xSpeed = speed * ((dst_x - x) / direction )
    ySpeed = speed * ((dst_y - y) / direction )
    return xSpeed, ySpeed


def moveDrone(src, dst):
    global SerialNumber
    params = {'SerialNumber': SerialNumber}
    print("Moving ...")
    src_x, src_y = src
    dst_x, dst_y = dst

    x, y = src
    Speed = 0.00001
    xSpeed, ySpeed = get_directions(src, dst, Speed)
    print(((dst_x - x)**2 + (dst_y - y)**2)**6)
    while ((dst_x - x)**2 + (dst_y - y)**2)*10**6 > 0.0002:
        x = x + xSpeed
        y = y + ySpeed
        with requests.Session() as session:
            current_location = {'x': x,
                                'y': y,
                                'status': 'Activate'
                                }
            print(current_location)
            resp = session.post(SERVER_URL, json=current_location, params=params)
        time.sleep(0.02)
    return (x, y)

def main():
    global SerialNumber
    params = {'SerialNumber': SerialNumber}
    current_coord = (13.1968122, 55.6882073)
    try:
        with open('location_save.txt', 'r') as file:
            data = file.readline().split(',')
            current_coord = (float(data[0]), float(data[1]))
    except:
        pass
    with requests.Session() as session:
        current_location = {'x': current_coord[0],
                            'y': current_coord[1],
                            'status': 'Idle'
                            }
        resp = session.post(SERVER_URL, json=current_location, params=params)
    dst_coord = current_coord
    geolocator = Nominatim(user_agent="my_request")
    region = ", Lund, Skåne, Sweden"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    server_address = ('0.0.0.0', 10000)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)
    while True:
        # Wait for a connection
        GET_ORDER = False
        print('waiting for a new connection')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(128)
                if len(data) < 5:
                    print('Invalide input')
                    break
                print('received destination address {!r}'.format(data.decode()))
                address = data.decode()
                print("Search address {}".format(address))
                dst_location = geolocator.geocode(address + region)
                if dst_location is None:
                    resp = "Could not find address {}, please try again".format(address)
                    print(resp)
                    resp_data = '0'
                    connection.sendall(resp_data.encode())
                else:
                    dst_coord = (dst_location.longitude, dst_location.latitude)
                    print(dst_coord)
                    resp = 'Found address, start delivering ...'
                    print(resp)
                    resp_data = '1'
                    resp = connection.sendall(resp_data.encode())
                    current_coord = moveDrone(current_coord, dst_coord)
                    with requests.Session() as session:
                        current_location = {'x': current_coord[0],
                                            'y': current_coord[1],
                                            'status': 'Idle'
                                            }
                        print(current_location)
                        resp = session.post(SERVER_URL, json=current_location, params=params)
                        print(resp)
                    resp = "Packet delivered to {}.".format(address)
                    connection.sendall(resp.encode())
                    with open('location_save.txt', 'w+') as file:
                        file.write(str(current_coord[0]) + ',' +  str(current_coord[1]))

        except KeyboardInterrupt:
            print("Unexpected error:", sys.exc_info()[0])
            connection.close()
            with open('location_save.txt', 'w+') as file:
                file.write(str(current_coord[0]) + ',' +  str(current_coord[1]))
            break



if __name__ == '__main__':
    global SerialNumber
    SerialNumber = getserialNumber()
    print("Serial Number: {}".format(SerialNumber))
    main()
