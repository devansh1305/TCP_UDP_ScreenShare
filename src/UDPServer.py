from socket import *
from threading import Thread
import sys
import numpy
import cv2
import pickle
import zlib
import mss

TCP = 0
UDP = 1

import tkinter as tk
root = tk.Tk()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

if len(sys.argv) < 2:
    connection_type = TCP
    port = 12345
    compression_level = 2
else:
    connection_type = sys.argv[1]
    port = sys.argv[2]
    compression_level = sys.argv[3]
    

'''

python3 server.py TCP PORT

python3 client.py TCP HOST PORT

server = TCPSERVER()

'''

clients = []

# create server socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', port))

# initiate server's ability to listen
server_socket.listen()
monitor = {"top": 0, "left": 0, "width": WIDTH, "height": HEIGHT}
# function used to continuously send frames
def send_frames():
    try:
        # loop to continousoly accept connections
        while True:
            # take a screenshot of current screen
            frame = numpy.array(mss.mss().grab(monitor))
            # serialize the frame
            data = zlib.compress(pickle.dumps(frame), compression_level)
            for client in clients:
                try:
                    # send the frame size to client
                    client.sendall((str(len(data)) + "\n").encode())
                    # send the serialized frame to client
                    client.sendall(data)
                except:
                    clients.remove(client)
                    print("removed a client from list of clients")
    except:
        return
t = Thread(target=send_frames, args=()).start()
try:
    # loop to continousoly accept connections
    while True:
        # accept connection
        connection_socket, addr = server_socket.accept()
        # call outer func to send frames
        clients.append(connection_socket)
        print("adding client to list of clients")
            
    # close server
#
except:
    server_socket.close()
    sys.exit(0)
