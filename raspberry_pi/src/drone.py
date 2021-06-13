from geopy.geocoders import Nominatim
import socket
import sys
import numpy as np
import time

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
        print(x, y)
        time.sleep(0.05)

    return (x, y)

def main():
    current_coord = (13.1968122, 55.6882073)
    dst_coord = current_coord
    geolocator = Nominatim(user_agent="my_request")
    region = ", Lund, Skåne, Sweden"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    server_address = ('0.0.0.0', 10000)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)
    try:

        while True:
            # Wait for a connection
            GET_ORDER = False
            print('waiting for a new connection')
            connection, client_address = sock.accept()
            try:
                print('connection from', client_address)
                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(32)
                    print('received destination address {!r}'.format(data.decode()))
                    address = data.decode()
                    print("Search address {}".format(address))
                    dst_location = geolocator.geocode(address + region)
                    dst_coord = (dst_location.longitude, dst_location.latitude)
                    print(dst_coord)
                    if dst_location is None:
                        resp = "Could find address {}, please try again".format(address)
                        print(resp)
                        connection.sendall(resp.encode())
                        # connection.close()
                        break
                    else:
                        # resp = 'Found address, start delivering ...'
                        # print(resp)
                        # resp = connection.sendall(resp.encode())
                        current_coord = moveDrone(current_coord, dst_coord)
                        resp = "Packet delivered to {}.".format(address)
                        print(resp)
                        connection.sendall(resp.encode())
            except:
                print("Unexpected error:", sys.exc_info()[0])
                connection.close()
    except KeyboardInterrupt:
        connection.close()

if __name__ == '__main__':
    SerialNumber = getserialNumber()
    print("Serial Number: {}".format(SerialNumber))
    main()
