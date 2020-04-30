import socket
import struct
import sys
import time
import mss
import mss.tools
import zlib
import pickle
import numpy
import cv2

# import tkinter as tk
# root = tk.Tk()
# WIDTH = root.winfo_screenwidth()
# HEIGHT = root.winfo_screenheight()

# monitor = {"top": 0, "left": 0, "width": WIDTH, "height": HEIGHT}

# frame = mss.mss().grab(monitor)

# cframe = zlib.compress(pickle.dumps(frame))


# data = numpy.array(frame)

# data = cv2.resize(data, (int(WIDTH * 0.75), int(HEIGHT * 0.75)))
# print(len(zlib.compress(pickle.dumps(data), 6)))


# multicast_group = '224.3.29.71'
# server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to
# the multicast group on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq)

# Receive/respond loop
while True:
    print('\nwaiting to receive message')
    num = ''
    data, address = sock.recvfrom(1024)
    print(data.decode())
    # while data.decode() != '\n':
    #     print(data.decode())
    #     num += data.decode()
    #     data, address = sock.recvfrom(1)
    data, address = sock.recvfrom(int(data.decode()))
    print('received {} bytes from {}'.format(
        len(data), address))
    print(data)

    print('sending acknowledgement to', address)
    sock.sendto(b'ack', address)
